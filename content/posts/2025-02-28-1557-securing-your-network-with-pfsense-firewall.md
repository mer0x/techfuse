---
title: "Securing your network with pfSense firewall"
date: 2025-02-28-1557
tags: ["Self-Hosting", "DevOps", "Homelab", "Networking"]
categories: ["IT Tutorials"]
draft: false
---

```markdown
---
title: "Securing Your Network with pfSense Firewall"
tags: ["pfSense", "Network Security", "Firewall", "Open Source", "Network Management"]
---

# Securing Your Network with pfSense Firewall

Securing your network is crucial in today's digital age where cyber threats are increasingly sophisticated. One of the most effective ways to safeguard your network is by implementing a robust firewall. pfSense, an open-source firewall software, offers comprehensive security features, scalability, and reliability, making it an excellent choice for both small and large networks. In this tutorial, we will explore how to secure your network using pfSense, with detailed steps and real-world examples.

## Prerequisites

Before diving into the implementation, ensure that you have the following prerequisites in place:

1. **Hardware Requirements**: 
    - A dedicated machine or virtual environment for pfSense installation. A low-power Intel or AMD processor with at least 1GB of RAM is recommended.
    - Two network interfaces (one for WAN and one for LAN) to interface with your network.

2. **pfSense Software**: 
    - Download the latest stable version of the pfSense ISO. You can obtain it from the official [pfSense website](https://www.pfsense.org/download/).

3. **Networking Knowledge**:
    - Understanding of basic networking concepts, including IP routing, subnets, and port forwarding.

## Implementation

### Step 1: Installing pfSense

1. **Boot from the pfSense ISO**:
   - Burn the pfSense ISO to a USB drive or CD and boot your machine from this media. You should be presented with a pfSense installation menu.

2. **Installation Steps**:
   - Select "Install" to start the installation process. Follow the prompts to configure disk partitions. Generally, the default options are sufficient.

3. **Network Configuration**:
   - After installation, configure the network interfaces. Assign the correct interface to WAN (typically the interface connected to your internet gateway) and LAN (the interface connected to your internal network).

4. **Assigning IP Addresses**:
   - Access the pfSense console and assign a static IP address to your LAN interface. For instance, `192.168.1.1/24` is commonly used as the LAN gateway.

### Step 2: Initial Configuration

1. **Access the Web Interface**:
   - Connect a device to your LAN. In a web browser, go to `http://192.168.1.1` to access the pfSense web interface.
   - Default credentials are `admin`/`pfsense`. Change these immediately for security purposes.

2. **Wizard Setup**:
   - Use the pfSense setup wizard to configure the basic firewall settings. Set a strong admin password, configure WAN type (DHCP or Static), and enable DHCP server on the LAN interface if necessary.

### Step 3: Configuring Firewall Rules

1. **Default Rules**:
   - pfSense includes default rules that block all inbound traffic on the WAN interface and allow all outbound from LAN. These settings preserve security for new installations.

2. **Creating Custom Rules**:
   - Navigate to **Firewall > Rules**. Under the **LAN** tab, create a new rule allowing DNS traffic:
   ```shell
   Interface: LAN
   Protocol: TCP/UDP
   Source: LAN Net
   Destination: LAN Address
   Destination Port Range: DNS (53)
   ```
   - For web browsing, allow HTTP/HTTPS traffic under LAN:
   ```shell
   Interface: LAN
   Protocol: TCP
   Source: LAN Net
   Destination: any
   Destination Port Range: HTTP (80) / HTTPS (443)
   ```

3. **Secure WAN Access**:
   - Limit WAN access by adding strict rules. For instance:
   ```shell
   Interface: WAN
   Protocol: TCP
   Source: any
   Destination: WAN Address
   Destination Port Range: OpenVPN (1194)
   ```
   This allows only VPN traffic through, ensuring secure remote access.

### Step 4: Configuring NAT (Network Address Translation)

1. **Port Forwarding**:
   - Suppose you host a web server on your network. To make it accessible externally, create a port forwarding rule:
   ```shell
   Interface: WAN
   Protocol: TCP
   Destination: WAN address
   Destination Port Range: HTTP (80)
   Redirect target IP: Internal Server IP (e.g., 192.168.1.100)
   Redirect Target Port: HTTP (80)
   ```

2. **Outbound NAT**:
   - Go to Firewall > NAT > Outbound and configure NAT based on your requirements. Automatic mode often suffices for most setups.

## Troubleshooting

1. **No Internet Access**:
   - Check cables, ensure correct interface assignment, and verify DHCP configurations.
   - Ensure firewall rules have been applied and DNS settings are correct.

2. **Firewall Rules Not Working**:
   - Check the order of firewall rules; pfSense processes rules from top to bottom.
   - Review logs under **Status > System Logs > Firewall** for blocked packets.

## Conclusion

pfSense offers a powerful set of features to manage and secure your network, providing the flexibility to configure firewall rules, NAT, and VPNs tailored to your needs. By following this tutorial, you now have a secure network setup capable of defending against external threats. Remember to regularly update pfSense and monitor your network for optimal security. Embrace the extensibility of pfSense to adapt your firewall configuration as networking needs evolve. Secure your network with confidence, knowing that pfSense is a steadfast guardian at its helm.
```
