from cliCodec.vsh import create_handle, conns
# import vsh
# import rex
import re
import os
import time
import webbrowser
import paramiko
import threading


def connectNE(handle, ip, user, pw, **args):
   
   """
    **Example**
   
    ::

       g40cli.connNEretry("cli1","172.17.1.80","secadmin","Infinera@1",retry=600)
        
       optional arg, step=False(default)|True(report a pixie/rex step)
         
       optional: port 2222 (sims for example)
         
       prompt ( and changable, sticky)
         
       optional: retry=600, retry for 600 seconds.
       default is 0, no retry.
    
    :param handle: Connection handle
    :type handle: string
    :param ip: NE IP address
    :type ip: string
    :param user: NE username
    :type user: string
    :param pw: NE password
    :type pw: string
    :return: True -> Pass, False -> Fail
    :rtype: boolean
    """   
   import ipdb; ipdb.set_trace()
#    try:
#     #    disconnect(handle)
#    except:
#        noop = 1
   retry = args.get("retry", 0)
   retry = int(retry)
    
   if retry == 0:
       try:
          rslt = _connNE_internal(handle, ip, user, pw, **args)
       except Exception as e:
          print("Exception raised while trying to connect: ", e)
          rslt = False
       if rslt is False:
           try:
               disconnect(handle)
           except:
               noop = 1
       else:
           return True
   else:
       retry = int(retry)
       t1 = time.time()
       t2 = t1 + retry
       while(time.time() < t2):
          try:
             rslt = _connNE_internal(handle, ip, user, pw, **args)
          except Exception as e:
             print("Exception raised while trying to connect: ", e)
             rslt = False
          if rslt is False:
             try:
                disconnect(handle)
             except:
                noop = 1
          else:
             return True
          print("Waiting 5 seconds before retrying connect...")
          time.sleep(5)
       print("Connect with retry timed-out")
       return False
           
def _connNE_internal(handle, ip, user, pw, **args):
    """
    **Example**

    ::

       g40cli.connectNE("cli1","172.17.1.80","secadmin","Infinera@1")
       
       optional arg, step=False(default)|True(report a pixie/rex step)
       optional: port, prompt ( and changable, sticky)
        

    :param handle: Connection handle
    :type handle: string
    :param ip: NE IP address
    :type ip: string
    :param user: NE username
    :type user: string
    :param pw: NE password
    :type pw: string
    :return: True -> Connected, False -> Connection Failed
    :rtype: Boolean
    """    
    
    #gCLI1 = rexui.App.conn1Frame()
    import ipdb; ipdb.set_trace()
    step = args.get("step", False)
    print(step)
    port = args.get("port", "22")
    print(port)
    print(handle, ip, user, pw)
    if create_handle(handle) is not None:
        if conns[handle].connect(ip, port, user, pw) == 1:
            #time.sleep(2)
            rslt = conns[handle].sendRcv("\n")
            print(rslt)
            rslt = conns[handle].sendRcv("show software-load\n")
            rslt = conns[handle].sendRcv("show inventory\n")
            rslt = conns[handle].sendRcv("show controller-card redundancy-status\n")
            rslt = conns[handle].sendRcv("\n")
            #rex.sleep(2)
            if rslt != 0:
               # if step:
               #    rex.step("g40cli.connect " + handle,"passed","prompt confirmed")
               return True
            else:
               # if step:
               #    rex.step("g40cli.connect " + handle,"failed","did not see prompt on connection")
               # else:
               #    print("Connect failed, did not see prompt for handle:", handle)
               return False
        else:
            # if step:
            #    rex.step("g40cli.connect " + handle,"failed","connect failed")
            # else:
            #    print("Connect failed for handle:", handle)
            return False

# def sendRcv(handle, cmd, **kwargs):
#     """

#     A method to send command to NE (CLI /SSH) and verify the prompt is returned.
#     The output from the command is returned as a string.

#     :param handle: handle string used with connect
#     :type handle: 
#     :param cmd: the command string to send on the cli, a \\n will be appended to this string. ( if this is not always desired, we will add an option to skip)
#     :type cmd: 
#     :return: None -> Fail, Actual result - Passed
#     :rtype: String

#    **Example**

#     ::
     
#          g40cli.sendRcv('cli1','show xcon')

#     :Optional parameters:
         
#       None
#    """    

#     # verify handle exists !!!

#     # pass along certain kwargs !!!
#     timeout = kwargs.get("timeout", 20)
#     timeout = int(timeout)
#     confirmI = kwargs.get("confirm", False)
#     step = kwargs.get("step", False)
#     match = kwargs.get("match", None)
#     poll = kwargs.get("poll", False)
#     stash = kwargs.get("stash", None)
#     mode = kwargs.get("mode", "ssh")
    
#     sendOnly=kwargs.get("sendOnly", False)
#     rcvOnly=kwargs.get("rcvOnly", False)
    
#     terminator = "\r" if mode == "telnet" else "\n"
    
#     # if normal send rcv ( btw should be in vsh layer)
#     # rcv only first, need timeout to be fast.
#     if rcvOnly is False:
#         vsh.conns[handle].sendRcv("not sending this", rcvOnly=True,timeout=0)
    
#     if confirmI:
#         cmdWn = cmd+terminator
#         rslt1 = vsh.conns[handle].sendRcv(cmdWn, sendOnly=True,**kwargs)
#         # should verify the y before continuing!!!
#         rslt = vsh.conns[handle].sendRcv('y'+terminator)
#         return rslt
#     else:
#         tnow = time.time()
#         tmax = tnow + int(timeout)
#         cmdWn = cmd+terminator
#         rslt = vsh.conns[handle].sendRcv(cmdWn,**kwargs)
#         print("result -",rslt,"-")
#         if match != None:
#             matchRslt = re.search(match,rslt,re.DOTALL)
#             if matchRslt is None:
#                 if poll is False:
#                    if step:
#                        rex.step("g40cli.sendRcv " + handle + " " + cmd,"failed","verify did not match result")
#                    if stash is not None:
#                       rex.stashData("set",stash,None)
#                    return None
#                 else:
#                    #kwargs = { "a":"b" , "timeout":100 }
#                    newL = kwargs.items()
#                    kwargs = {}
#                    for a,v in newL:
#                       if a != "timeout":
#                          kwargs[a] = v
#                       else:
#                          # timeout / command hard coded to 30 sec / iteration for now
#                          kwargs[a] = 30
#                    while tnow < tmax:
#                       #print("tnow tmax",tnow," ",tmax)
#                       #print("Poll wait 5 sec - ",end='')
#                       cont = rex.sleep(5,newline=False)
#                       if cont is False:
#                          # 
#                          if step:
#                             rex.step("g40cli.sendRcv " + handle + " " + cmd,"aborted","")
#                          return None
#                       rslt = vsh.conns[handle].sendRcv(cmdWn,**kwargs)
#                       matchRslt = re.search(match,rslt,re.DOTALL)
#                       if matchRslt is None:
#                          # keep trying
#                          noop = 1
#                          ret = None
#                       else:
#                          ret = matchRslt.group()
#                          if step:
#                             rex.step("g40cli.sendRcv " + handle + " " + cmd,"passed","verify matched result")
#                          return ret
#                       if vsh.sim("get"):
#                          if step:
#                             rex.step("g40cli.sendRcv " + handle + " " + cmd,"passed","sim verify matched result")
#                          return "sim str"   
#                       tnow = time.time()
#                    rex.log("")
#                    if step:
#                       rex.step("g40cli.sendRcv " + handle + " " + cmd,"failed","verify matched result")
#                    return ret
#                    # if got here, failed:
#                    if step:
#                       rex.step("g40cli.sendRcv " + handle + " " + cmd,"failed","verify did not match result")
#                    return None
#             else:
#                # check none
#                ret = matchRslt.group()
#                if step:
#                    rex.step("g40cli.sendRcv " + handle + " " + cmd,"passed","verify matched result")
#                if stash is not None:
#                   rex.stashData("set",stash,ret)
#                return ret
#         else:
#             if step:
#                if rslt is "0":
#                   rex.step("g40cli.sendRcv " + handle + " " + cmd,"failed","prompt not returned")
#                else:
#                   rex.step("g40cli.sendRcv " + handle + " " + cmd,"passed","prompt returned")
#             if stash is not None:
#                rex.stashData("set",stash,rslt)
#             return rslt


def disconnect(handle,step=False):
   
   """     
   disconnect("<handle name>"): Method to close a session by its handle name. The handles are created by create_handle function 

   **Example**
                  
      ::    

          disconnect('cli1')  # closes a session with handle name 'cli1'
            
          disconnect('netconf1')  # closes a session with handle name 'netconf1'
            
          disconnect('all')  # closes ALL sessions which are active

   :param handle: session handle name - This is the session handle created by **create_handle()** method
   :type handle: string
   :param step: _description_, defaults to False
   :type step: bool, optional
   """   
   rslt = vsh.disconnect(handle)
   # if step:
   #      #rex.step("Disconnect: "+handle,"passed")   #CPIXIS
   
   return rslt
