"""
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

"""


import math


class SubnetterFunctions:
    """Basic repeatable functions that are used to calculate the parameters"""

    def __init__(self):
        pass

    def calc_hosts_cidr(self, cidr):
        if cidr == 32:
            hosts = 1
        elif cidr == 31:
            hosts = 1
        else:
            hosts = (2 ** (32 - cidr)) - 2
        return hosts

    def calc_mask_cidr(self, cidr):
        if 24 <= cidr <= 32:
            octet4 = (256 - 2 ** (32 - cidr))
            octet2 = 255
            octet3 = 255
        elif 16 <= cidr < 24:
            octet3 = (256 - 2 ** (24 - cidr))
            octet2 = 255
            octet4 = 0
        elif 8 <= cidr < 16:
            octet2 = (256 - 2 ** (16 - cidr))
            octet3 = 0
            octet4 = 0
        mask = f"255.{octet2}.{octet3}.{octet4}"
        return mask

    def calc_subnets_cidr(self, cidr):
        if 24 <= cidr <= 32:
            subnets = 2 ** (8 - (32 - cidr))
        elif 16 <= cidr < 24:
            subnets = 2 ** (16 - (32 - cidr))
        elif 8 <= cidr < 16:
            subnets = 2 ** (24 - (32 - cidr))
        return subnets


netfx = SubnetterFunctions()


class Subnetter:

    def __init__(self):
        self.subnets = 0
        self.hosts = 0
        self.cidr = 0
        self.mask = []
        self.netaddr = []

    def set_subnets(self, subnets, class_var):
        """Use to set the parameter: subnets.
           subnets must be an integer between 1 and 128.
           class_var must be a string. Use one of the following: 'a', 'b', 'c'"""

        # Set number of subnets based on user input.
        if subnets < 1 or subnets > 128:
            print("Number of subnets must be between 1 and 128.")
            exit()
        y = 1
        while subnets > y:
            y *= 2
        self.subnets = y

        # Calculate CIDR based on subnets.
        if class_var.lower() == "c":
            self.cidr = int(32 - math.log(256 / self.subnets) / math.log(2))
        elif class_var.lower() == "b":
            self.cidr = int(24 - math.log(256 / self.subnets) / math.log(2))
        elif class_var.lower() == "a":
            self.cidr = int(16 - math.log(256 / self.subnets) / math.log(2))

        # Use CIDR to calculate number of hosts per subnet. Run calc_hosts_cidr from SubnetterFunctions class.
        self.hosts = netfx.calc_hosts_cidr(self.cidr)

        # Use CIDR to calculate the subnet mask. Run calc_mask_cidr from SubnetterFunctions class.
        self.mask = netfx.calc_mask_cidr(self.cidr)

    def set_hosts(self, hosts):
        """Use to set the parameter: hosts.
           hosts must be an integer between 1 and 16777214."""

        # Set hosts based on user input.
        if hosts < 1 or hosts > 16777214:
            print("Please enter a value between 1 and 16,777,214")
            exit()
        hosts += 2
        y = 1
        while hosts > y:
            y *= 2
        self.hosts = y - 2

        # Calculate CIDR based on number of hosts per subnet.
        self.cidr = int(32 - math.log(self.hosts + 2) / math.log(2))

        # Calculate subnets based on CIDR. Run calc_subnets_cidr from SubnetterFunctions class.
        self.subnets = netfx.calc_subnets_cidr(self.cidr)

        # Calculate mask based on CIDR. Run calc_mask_cidr from SubnetterFunctions class.
        self.mask = netfx.calc_mask_cidr(self.cidr)

    def set_mask(self, mask):
        """Use to set the parameter: mask.
           mask must be a valid subnet mask in string type. Ex. '255.255.255.0'"""

        # Set mask based on user input.
        self.mask = mask

        # Calculate CIDR based on mask. The significant octet is found first. Then CIDR is calculated based on
        # the significant octet.
        mask = mask.split(".")
        if len(mask) != 4:
            print("Enter a valid subnet mask.")
            exit()
        int_mask = []
        for octet in mask:
            int_mask.append(int(octet))
        octet_list = [255, 254, 252, 248, 240, 224, 192, 128, 0]
        for octet in int_mask:
            if octet not in octet_list:
                print("Enter a valid subnet mask.")
                exit()
        for octet in int_mask:
            if 0 < octet < 255:
                significant_octet = octet
                break
        else:
            if int_mask[3] == 255:
                significant_octet = 255
            else:
                significant_octet = 0
        if int_mask[1] < 255:
            self.cidr = int(16 - math.log(256 - significant_octet) / math.log(2))
        elif int_mask[2] < 255:
            self.cidr = int(24 - math.log(256 - significant_octet) / math.log(2))
        else:
            self.cidr = int(32 - math.log(256 - significant_octet) / math.log(2))

        # Calculate subnets based on CIDR. Run calc_subnets_cidr from SubnetterFunctions class.
        self.subnets = netfx.calc_subnets_cidr(self.cidr)

        # Calculate hosts based on CIDR. Run calc_hosts_cidr from SubnetterFunctions class.
        self.hosts = netfx.calc_hosts_cidr(self.cidr)

    def set_cidr(self, cidr):
        """Use to set parameter: cidr.
           cidr must be an integer between 8 and 32."""

        # Set CIDR value based on user input.
        if not 8 <= cidr <= 32:
            print("Please enter a CIDR value between 8 and 32.")
            exit()
        self.cidr = cidr

        # Calculate subnets based on CIDR. Run calc_subnets_cidr from SubnetterFunctions class.
        self.subnets = netfx.calc_subnets_cidr(self.cidr)

        # Calculate hosts based on CIDR. Run calc_hosts_cidr from SubnetterFunctions class.
        self.hosts = netfx.calc_hosts_cidr(self.cidr)

        # Calculate mask based on CIDR. Run calc_mask_cidr from SubnetterFunctions class.
        self.mask = netfx.calc_mask_cidr(self.cidr)

    def print_output(self):
        """Print out values for the 4 parameters: subnets, hosts, mask, cidr"""
        print(f"CIDR: /{self.cidr}")
        print(f"Subnet Mask: {self.mask}")
        print(f"Number of Subnets: {self.subnets}")
        print(f"Hosts per Subnet: {self.hosts}  (Excludes network and broadcast addresses.)")

    def get_netaddr(self):
        """Outputs a list of network addresses.
           Ex. 255.255.255.128 has 2 network addresses: ['0', '128']
           Must use one of the set_parameter functions beforehand."""
        if self.cidr == 0:
            print("Set a parameter before running get_netaddr. Use set_subnets, set_hosts, set_mask, or set_cidr")
            exit()
        else:
            print("\nNetwork addresses:")
            if 24 <= self.cidr <= 32:
                print("(Place in 4th octet)")
                addr_gap = 2 ** (32 - self.cidr)
            elif 16 <= self.cidr < 24:
                print("(Place in 3rd octet)")
                addr_gap = 2 ** (24 - self.cidr)
            elif 8 <= self.cidr < 16:
                print("(Place in 2nd octet)")
                addr_gap = 2 ** (16 - self.cidr)
            addr_list = []
            net_addr = 0
            while net_addr < 256:
                addr_list.append(net_addr)
                net_addr += addr_gap
            print(addr_list)
            self.netaddr = addr_list

