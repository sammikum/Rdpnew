flowchart TD
  A[Trigger: workflow_dispatch / schedule (every 6h)] --> B[Windows runner (windows-latest)]
  B --> C[Download files]
  C --> C1[setup.py]
  C --> C2[Avica_setup.exe]
  C --> C3[show.bat / loop.bat]
  B --> D[Install Python packages]
  D --> D1[requests, pyautogui, telegraph]
  B --> E[Enable RDP & Firewall]
  E --> E1[Set registry fDenyTSConnections = 0]
  E --> E2[Enable-NetFirewallRule 'Remote Desktop']
  B --> F[Set user password]
  F --> F1[net user runneradmin TheDisa1a]
  B --> G[Start Avica]
  G --> G1[Start-Process Avica_setup.exe]
  G --> G2[python setup.py]
  B --> H[Show Connection Info]
  H --> I[run show.bat => prints banner + waits for GoFile link]
  B --> J[Keep session active]
  J --> J1[run loop.bat => infinite loop / periodic activity]
  J --> K[Job runs until timeout-minutes (350) or terminated]

  style A fill:#f9f,stroke:#333,stroke-width:1px
  style K fill:#fdd,stroke:#333,stroke-width:1px
