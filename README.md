# subnetter
Subnet Calculator - personal project

Subnetter is simply a subnet calculater. It works off the premise that each subnet has 4 parameters associated
with it. These 4 parameter are:

    1. number of available subnets (referred to as 'subnets')
        ex. 255.255.255.128 has 2 available class C subnets.

    2.  number of hosts per subnet ('hosts')
        ex. 255.255.255.128 has 126 hosts available per subnet (excluding the network and broadcast addresses).

    3. subnet mask ('mask')
        ex. 255.255.255.128

    4. CIDR notation ('cidr')
        ex. /25

Subnetter has the user set one of the above parameters, then calculates the other 3 based on that one parameter.
ex. We need 126 hosts per subnet. So we call the funtion 'set_hosts(126)'.
    Subnetter then calculates subnets, mask, and cidr based on a subnet with 126 available hosts.

There are 4 functions to set the parameters:

    1. set_subnets(subnets, class_var)
        - Enter subnets as an integer. Ex. 32
        - Enter class_var as a string. Ex. 'a', 'b', or 'c'

    2. set_hosts(hosts)
        - Enter hosts as an integer. Ex. 24

    3. set_mask(mask)
        - Enter mask as a string. Ex. '255.255.255.0'

    4. set_cidr(cidr)
        - Enter cidr as an integer. Ex. 24

Once a parameter is set, the values can be viewed by calling the 'print_output()' function.

The 'get_netaddr()' function creates a list of network addresses related to the subnet.
Ex. A /25 mask has the following network address: x.x.x.0 , x.x.x.128
    So the get_netaddr output will be a list as follows: (In 4th octet) ['0', '128'].
