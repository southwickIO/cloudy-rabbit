#!/usr/bin/env python3



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NAME: dk.py                                                                 #
#                                                                             #
# VERSION: 20230415                                                           #
#                                                                             #
# SYNOPSIS: Sniff out potential ACK tunneling                                 #
#                                                                             #
# DESCRIPTION: This script looks for potential indicators of ACK tunelling.   #
#              ACK tunneling is a technique used in network security to       #
#              bypass firewalls and other network security devices that use   #
#              stateful packet inspection. The technique involves             #
#              encapsulating data within ACK packets, which are typically     #
#              used to acknowledge the receipt of data packets. The top 5     #
#              indicators of ACK tunneling are:                               #
#              1.) Suspicious traffic patterns                                #
#              2.) Large amounts of data transferred through ACK packets      #
#              3.) Encrypted or encoded data within ACK packets               #
#              4.) Repeated use of the same ACK packet number                 #
#              5.) Unusual TCP header flags                                   #
#                                                                             #
# INPUT: None                                                                 #
#                                                                             #
# OUTPUT: STDOUT                                                              #
#                                                                             #
# PRE-RUNTIME NOTES: None                                                     #
#                                                                             #
# AUTHORS: @southwickio                                                       #
#                                                                             #
# LICENSE: GPLv3                                                              #
#                                                                             #
# DISCLAIMER: All work produced by Authors is provided “AS IS”. Authors make  #
#             no warranties, express or implied, and hereby disclaims any and #
#             all warranties, including, but not limited to, any warranty of  #
#             fitness, application, et cetera, for any particular purpose,    #
#             use case, or application of this script.                        #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #



#import dependencies
import socket
import struct



#define variables
prevacknum = 0



#define functions
def printIndicators(pkt):
    '''
    This function takes a packet as input and parses its IP and TCP headers. It
    then checks for various indicators of ACK tunneling using the other
    functions. If an indicator is triggered, it prints the corresponding
    message along with the source and destination IP addresses.
    '''



    #parse IP header
    iphdr = pkt[0 : 20] #first 20 bytes (IP header)
    iph = struct.unpack('!BBHHHBBH4s4s', iphdr) #create tuple breakdown

    '''
    iph breakdown:
    iph[0]: IP version and header length.
    iph[1]: Type of service.
    iph[2]: Total length of the packet (header + data).
    iph[3]: Identification.
    iph[4]: Flags and fragmentation offset.
    iph[5]: Time to live.
    iph[6]: Protocol (TCP, UDP, etc.).
    iph[7]: Header checksum.
    iph[8]: Source IP address.
    iph[9]: Destination IP address.
    '''

    srcip = socket.inet_ntoa(iph[8])
    dstip = socket.inet_ntoa(iph[9])



    #parse TCP header
    iphlen = iph[0] & 0xF #first four bits
    tcph = struct.unpack('!HHLLBBHHH', pkt[iphlen * 4:iphlen * 4 + 20]) 

    '''
    tcph breakdown:
    tcph[0]: Source port number.
    tcph[1]: Destination port number.
    tcph[2]: Sequence number.
    tcph[3]: Acknowledgment number.
    tcph[4]: Data offset, reserved bits, and flags.
    tcph[5]: TCP flags.
    tcph[6]: Window size.
    tcph[7]: Checksum.
    tcph[8]: Urgent pointer.
    '''

    acknum = tcph[2]
    tcpflags = tcph[5]



    # Check for indicators of ACK tunneling
    if suspiciousTrafficPattern(pkt):

        print(f"Suspicious traffic pattern detected: src={srcip}, dst={dstip}")



    if largeAmountOfDataTransferred(pkt):

        print(f"Large amount of data transferred through ACK packets: \
            src={srcip}, \
            dst={dstip}")



    if EncryptedOrEncodedData(pkt, iphlen):

        print(f"Encrypted or encoded data within ACK packets: \
            src={srcip}, \
            dst={dstip}")



    if RepeatedAcknum(pkt, iphlen):

        print(f"Repeated use of the same ACK packet number: \
            src={srcip}, \
            dst={dstip}")



    if UnusualTcpFlags(pkt):

        print(f"Unusual TCP header flags detected: src={srcip}, dst={dstip}")



def suspiciousTrafficPattern(pkt):
    '''
    This function checks if the packet has a small size and is a TCP ACK packet
    without data. If this condition is met, it returns True, indicating that a
    suspicious traffic pattern has been detected.
    '''

    '''
    The return statement does the following:
    1.) len(pkt) < 64: This condition checks if the length of the packet is
        less than 64 bytes. This is because ACK packets without data are
        typically small in size.
    2.) (pkt[13] & 0x18) == 0x10: This condition checks if the ACK flag is set
        in the TCP header. The ACK flag is represented by the third bit from
        the right in the 14th byte of the TCP header. The hexadecimal value
        0x10 corresponds to the binary value 00010000, which has the third bit
        set to 1.
    3.) len(pkt) == struct.unpack('!H', pkt[2:4])[0] 
        - (4 * (pkt[0] & 0x0f) + 4 * (pkt[12] >> 4)): This condition checks if
        the length of the packet matches the expected length based on the TCP
        header fields. The expected length is calculated as follows:
        a.) The total length field in the IP header minus the IP header length
            minus the TCP header length (i.e., the length of the TCP data).
        b.) The total length field is located in bytes 2-3 of the IP header and
            is in network byte order (big-endian), so we use struct.unpack() to
            extract it.
        c.) The IP header length field is the first 4 bits of the first byte of
            the IP header, which we extract using the bitwise AND operator &
            with the value 0x0f. This gives us a value in the range 0-15, which
            we multiply by 4 to get the actual length in bytes.
        d.) The TCP header length field is the first 4 bits of the 13th byte of
            the TCP header, which we extract using the bitwise shift operator
            >> with the value 4. This gives us a value in the range 0-15, which
            we multiply by 4 to get the actual length in bytes.
        e.) We then subtract the sum of the IP header length and TCP header
            length from the total length to get the expected length of the TCP
            data.
    If all three conditions are true, then the line returns True, indicating
    that a suspicious traffic pattern has been detected in the TCP ACK packet.
    '''

    return len(pkt) < 64 \
    and (pkt[13] & 0x18) == 0x10 \
    and len(pkt) == struct.unpack('!H', pkt[2 : 4])[0] \
    - (4 * (pkt[0] & 0x0f) + 4 * (pkt[12] >> 4))



def largeAmountOfDataTransferred(pkt):
    '''
    This function checks if the packet has a large data size within the ACK
    flag. If this condition is met, it returns True, indicating that a large
    amount of data has been transferred through ACK packets.
    '''

    '''
    The return statement does the following:
    1.) (pkt[13] & 0x18) == 0x10: This condition checks if the ACK flag is set
        in the TCP header. The ACK flag is represented by the third bit from
        the right in the 14th byte of the TCP header. The hexadecimal value
        0x10 corresponds to the binary value 00010000, which has the third bit
        set to 1.
    2.) (struct.unpack('!H', pkt[2:4])[0] - 
        (4 * (pkt[0] & 0x0f) + 4 * (pkt[12] >> 4))) > 64: This condition checks
        if the length of the TCP data in the packet is greater than 64 bytes.
        The length of the TCP data is calculated as follows:
        a.) The total length field in the IP header minus the IP header length
            minus the TCP header length (i.e., the length of the TCP data).
        b.) The total length field is located in bytes 2-3 of the IP header
            and is in network byte order (big-endian), so we 
            use struct.unpack() to extract it.
        c.) The IP header length field is the first 4 bits of the first byte
            of the IP header, which we extract using the bitwise AND operator &
            with the value 0x0f. This gives us a value in the range 0-15, which
            we multiply by 4 to get the actual length in bytes.
        d.) The TCP header length field is the first 4 bits of the 13th byte of
            the TCP header, which we extract using the bitwise shift operator
            >> with the value 4. This gives us a value in the range 0-15, which
            we multiply by 4 to get the actual length in bytes.
        e.) We then subtract the sum of the IP header length and TCP header
            length from the total length to get the length of the TCP data.
        f.) We then check if the length of the TCP data is greater than 64
            bytes.
    If both conditions are true, then the line returns True, indicating that a
    large amount of data has been transferred through ACK packets.
    '''

    return (pkt[13] & 0x18) == 0x10 \
    and (struct.unpack('!H', pkt[2 : 4])[0] \
        - (4 * (pkt[0] & 0x0f) + 4 * (pkt[12] >> 4))) > 64



def EncryptedOrEncodedData(pkt, iphlen):
    '''
    This function checks if the packet data is encoded or encrypted. If this
    condition is met, it returns True, indicating that encrypted or encoded
    data has been detected within ACK packets.
    '''

    '''
    The return statement does the following:
    1.) (pkt[13] & 0x18) == 0x10: This condition checks if the ACK flag is set
        in the TCP header. The ACK flag is represented by the third bit from
        the right in the 14th byte of the TCP header. The hexadecimal value
        0x10 corresponds to the binary value 00010000, which has the third bit
        set to 1.
    2.) pkt[iphlen * 4 + 20:] != b'\x00'*len(pkt[iphlen * 4 + 20:]): This 
        condition checks if the TCP data in the packet is not all null bytes.
    The iphlen * 4 + 20 index is used to skip over the IP and TCP headers and
    get to the start of the TCP data in the packet. We then compare the TCP
    data to a sequence of null bytes (b'\x00') of the same length. If the TCP
    data is not all null bytes, it could be because the data is encrypted or
    encoded.

    If both conditions are true, then the line returns True, indicating that
    encrypted or encoded data has been detected within ACK packets.
    '''

    return (pkt[13] & 0x18) == 0x10 \
    and pkt[iphlen * 4 + 20:] != b'\x00'*len(pkt[iphlen * 4 + 20:])







def RepeatedAcknum(pkt, iphlen):
    '''
    This function checks if the packet ACK number is repeated. It keeps track
    of the previous ACK number seen and compares it to the current ACK number.
    If they are the same, it returns True, indicating that a repeated ACK
    number has been detected.
    '''
    
    #declare variables
    global prevacknum#declared global so previous packet can access number
    acknum = struct.unpack('!L', \
        pkt[iphlen * 4 + 8:iphlen * 4 + 12])[0]

    '''
    acknum is doing the following:
    1.) This line of code is extracting the acknowledgment number from the TCP
        header of a packet and storing it in the acknum variable.
    2.) The acknowledgment number is a 32-bit value that represents the next
        expected sequence number of a TCP connection. It is used to
        acknowledge receipt of data and to signal to the sender that the 
        receiver is ready to receive more data.
    3.) The struct.unpack() function is used to unpack the acknowledgment
        number from the packet. The format string '!L' specifies that we want
        to unpack a 32-bit unsigned integer in network byte order (big-endian).
    4.) The expression pkt[iphlen * 4 + 8:iphlen * 4 + 12] is used to
        slice the TCP header from the packet and extract the acknowledgment
        number. The index iphlen * 4 + 8 points to the start of the
        acknowledgment number field in the TCP header, and the index
        iphlen * 4 + 12 points to the end of the acknowledgment number
        field.
    5.) The [0] at the end of the line is used to access the first (and only)
        element of the resulting tuple returned by struct.unpack(). Since we
        are unpacking a single 32-bit integer, the resulting tuple contains a
        single element, which is the acknowledgment number itself.
    '''



    #check for same acknum
    if prevacknum and acknum == prevacknum:

        prevacknum = acknum



        return True



    prevacknum = acknum



    return False



def UnusualTcpFlags(pkt):    
    '''
    This function checks if the packet has unusual TCP flags set. Specifically,
    it checks if the ACK, FIN, and PUSH flags are set in a way that is not
    typical of normal traffic. If this condition is met, it returns True,
    indicating that unusual TCP header flags have been detected.
    '''
    
    '''
    The return statement does the following:
    1.) The TCP header consists of several 4-bit fields, including the 6
        reserved bits located in the 13th byte of the header. These bits are
        reserved for future use and should always be set to 0.
    2.) The expression (pkt[13] & 0x38) is used to extract the 3 reserved bits
        (i.e., bits 3-5) from the TCP header and check if their values are
        unusual. The hexadecimal value 0x38 corresponds to the binary value
        00111000, which has bits 3-5 set to 1 and bits 0-2 set to 0.
    3.) Checks if the value of the 3 reserved bits is not equal to 0x10
        (binary 00100000) or 0x18 (binary 00110000). These values are unusual
        for the reserved bits and could indicate abnormal behavior or an
        attempt to manipulate the TCP header.
    4.) If either of the conditions is true (i.e., the reserved bits are not
        set to the expected values), then the line returns True, indicating
        that unusual TCP header flags have been detected in the packet.
    '''

    return (pkt[13] & 0x38) != 0x10 and (pkt[13] & 0x38) != 0x18



#create a raw socket and bind it to all interfaces
rawsocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
rawsocket.bind(('0.0.0.0', 0))

'''
The above code code creates a raw socket that listens to all incoming TCP 
traffic on all network interfaces of the local machine.
A raw socket is a network socket that allows direct access to network protocols
at the transport layer (e.g., TCP, UDP). Unlike a regular socket, which is 
typically used to communicate with a specific remote host and port, a raw 
socket can be used to capture and manipulate network packets at a lower level.
The socket.socket() function is used to create a new raw socket object. The 
socket.AF_INET argument specifies that we want to use the IPv4 address family,
and the socket.SOCK_RAW argument specifies that we want to use a raw socket.
The socket.IPPROTO_TCP argument specifies that we want to listen for TCP
traffic specifically.
The rawsocket.bind(('0.0.0.0', 0)) line binds the raw socket to all network
interfaces on the local machine by specifying the IP address '0.0.0.0' and the
port number 0. Binding the socket to port 0 allows the operating system to
assign an available port number automatically.
'''



#inspect packets
while True:
    pkt, addr = rawsocket.recvfrom(65536)
    printIndicators(pkt)