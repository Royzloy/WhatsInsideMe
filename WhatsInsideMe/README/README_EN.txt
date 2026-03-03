╔╗╔╗╔╗╔╗╔╗╔══╗╔════╗╔══╗╔══╗╔╗─╔╗╔══╗╔══╗╔══╗─╔═══╗╔╗──╔╗╔═══╗
║║║║║║║║║║║╔╗║╚═╗╔═╝║╔═╝╚╗╔╝║╚═╝║║╔═╝╚╗╔╝║╔╗╚╗║╔══╝║║──║║║╔══╝
║║║║║║║╚╝║║╚╝║──║║──║╚═╗─║║─║╔╗─║║╚═╗─║║─║║╚╗║║╚══╗║╚╗╔╝║║╚══╗
║║║║║║║╔╗║║╔╗║──║║──╚═╗║─║║─║║╚╗║╚═╗║─║║─║║─║║║╔══╝║╔╗╔╗║║╔══╝
║╚╝╚╝║║║║║║║║║──║║──╔═╝║╔╝╚╗║║─║║╔═╝║╔╝╚╗║╚═╝║║╚══╗║║╚╝║║║╚══╗
╚═╝╚═╝╚╝╚╝╚╝╚╝──╚╝──╚══╝╚══╝╚╝─╚╝╚══╝╚══╝╚═══╝╚═══╝╚╝──╚╝╚═══╝

WhatsInsideMe - a simple tool that gathers all essential information about your computer.

Features:
- CPU model, load, core counts
- RAM (total, used, available)
- Hard drives (partitions, used space)
- Network interfaces (IP, MAC)
- Graphics card (model, memory, temperature) — if present
- Monitors (resolution, name)
- Audio devices
- Battery info (for laptops)
- Report timestamp

Saving reports:
You can save the collected info as .txt, .html, or .pdf via the File -> Save as... menu.
Printing:
The File menu also has a Print option — it opens the standard Windows print dialog (or pipes to lp on Linux/Mac).

How to use:
1. Download WhatsInsideMe.exe
2. run file
3. After a couple of seconds, you'll see your system info.
4. Click the Refresh button on the toolbar to reload the data.
5. To exit, just close the window or use File\Exit

Antivirus & safety:
Some antivirus engines (notably Bkav Pro, SecureAge) may flag this .exe as suspicious. This is a known false positive caused by PyInstaller (the tool used to package the program) producing self‑extracting executables that can resemble malware behaviour. The source code is fully transparent and the program does nothing but read system information.

If you are a paranoid person and don't trust a pre‑built executable - well, just don't download it. You can check the source code, it's right there alongside the program. If you did download and your AV complains, add the file to exceptions or choose "Run anyway".

Version: 26.1.2 (2026)
Crafted with Python using psutil, gputil, screeninfo, sounddevice, fpdf.

Feedback and suggestions: matveybankovproduct@gmail.com