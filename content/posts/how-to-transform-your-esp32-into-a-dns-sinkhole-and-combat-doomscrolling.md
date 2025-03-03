---
ShowBreadCrumbs: true
ShowPostNavLinks: true
ShowReadingTime: true
ShowRssButtonInSectionTermList: true
ShowWordCount: true
TocOpen: false
UseHugoToc: true
author: Auto Blog Generator
comments: true
date: '2025-03-03'
description: A guide on Turning my ESP32 into a DNS sinkhole to fight doomscrolling
disableHLJS: false
disableShare: false
draft: false
hideSummary: false
hidemeta: false
searchHidden: false
showToc: true
tags:
- ESP32
- DNS sinkhole
- doomscrolling
- digital wellbeing
- Arduino
title: How to Transform Your ESP32 into a DNS Sinkhole and Combat Doomscrolling
---

In the digital age, doomscrolling has emerged as a pervasive issue, with countless individuals finding themselves lost in endless scrolls through negative news and social media feeds. This habit not only consumes precious time but also impacts mental health. Fortunately, technology offers a myriad of solutions to tackle this problem. One such innovative solution is converting an ESP32 microcontroller into a DNS sinkhole. This post will guide you through the process step by step, providing a practical way to limit doomscrolling by blocking access to time-sinking websites.

## Why Does This Matter?

The ESP32, a low-cost, low-power system on a chip microcontroller with integrated Wi-Fi and dual-mode Bluetooth, offers a perfect platform for DIY projects aimed at improving digital wellbeing. By setting up a DNS sinkhole, you can intercept DNS requests for specific domains (like social media sites) and reroute them to a local IP address that serves a block page, effectively preventing access. This not only helps in reducing doomscrolling but also enhances productivity and focuses by minimizing distractions.

## Step-by-Step Guide to Setting Up Your DNS Sinkhole

### Prerequisites

- An ESP32 board
- A USB cable to connect your ESP32 to your computer
- Arduino IDE installed on your computer
- Basic understanding of DNS and networking concepts

### Step 1: Preparing Your ESP32

1. Connect your ESP32 to your computer using the USB cable.
2. Open the Arduino IDE and install the ESP32 board manager. Go to File > Preferences, and in the "Additional Board Manager URLs" field, add the ESP32 board manager URL (you can find the latest URL from the espressif GitHub page).
3. Open the Board Manager by navigating to Tools > Board > Boards Manager, search for ESP32, and install it.

### Step 2: Installing Required Libraries

For this project, we'll need a couple of libraries:
- **DNSServer** — for handling DNS requests
- **WebServer** — to serve the block page

These libraries usually come pre-installed with the ESP32 board manager. If not, you can find them in the Library Manager (Sketch > Include Library > Manage Libraries).

### Step 3: Configuring Your DNS Sinkhole

Below is a basic sketch that sets up your ESP32 as a DNS sinkhole. Copy the code into your Arduino IDE:

```cpp
#include <WiFi.h>
#include <DNSServer.h>
#include <WebServer.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

DNSServer dnsServer;
WebServer webServer(80);

const byte DNS_PORT = 53;
IPAddress apIP(192, 168, 4, 1);

void setup() {
  Serial.begin(115200);
  
  WiFi.softAP(ssid, password);
  delay(500); // Allow the AP to start

  dnsServer.start(DNS_PORT, "*", apIP);
  
  webServer.onNotFound([]() {
    webServer.send(200, "text/html", "<h1>This site is blocked.</h1>");
  });
  
  webServer.begin();
}

void loop() {
  dnsServer.processNextRequest();
  webServer.handleClient();
}
```

Replace `"YOUR_SSID"` and `"YOUR_WIFI_PASSWORD"` with your desired network name and password. This code creates a Wi-Fi access point and redirects all DNS requests to the specified IP address, where a simple web server delivers a block page.

### Step 4: Flashing Your ESP32

After configuring the sketch:
1. Select the correct ESP32 board from Tools > Board.
2. Choose the correct COM port under Tools > Port.
3. Click the Upload button.

Once the sketch is uploaded, your ESP32 will start functioning as a DNS sinkhole.

### Step 5: Connecting to Your DNS Sinkhole

On your device (e.g., smartphone or laptop):
1. Connect to the Wi-Fi network created by your ESP32.
2. Try accessing any website. You should be greeted with the block page served by your ESP32.

## Conclusion

By following the steps outlined above, you've successfully turned your ESP32 into a DNS sinkhole, providing a powerful tool to combat doomscrolling and enhance digital wellbeing. This project not only showcases the versatility of the ESP32 but also demonstrates a practical application of networking concepts. Remember, while technology can aid in reducing distractions, personal discipline and mindfulness play a crucial role in managing digital consumption effectively.

Feel free to customize the block page and expand the functionality of your DNS sinkhole by adding authentication, logging, or more sophisticated domain filtering rules.

Key takeaways include understanding the basics of DNS operations, the utility of the ESP32 microcontroller in networking projects, and the potential of DIY solutions in addressing everyday challenges.