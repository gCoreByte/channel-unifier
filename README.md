<p align="center">
    <h1 align="center">channel-unifier</h1>
    <h3 align="center">A Python script to do what your TAs should've done long ago: use a single place to communicate.</h3>
</p>

# Simple to use
Built from the ground up with usage in mind, the script is runnable on any machine that supports Python 3. It requires no database or special permissions.

## Configuration
All the configuration is in the `/config` folder, which contains a config file for every supported integration. Simply make a copy, rename the `.example` extension and fill in the required data.

# Supported apps
| Supported | Application |                                                                  |
|-----------|-------------|------------------------------------------------------------------|
| Partially | Discord     | Currently includes sending to webhooks, does not support reading |
| Yes       | Zulip       |                                                                  |
| Planned   | Slack       |                                                                  |
| Planned   | CampusWire  |                                                                  |

