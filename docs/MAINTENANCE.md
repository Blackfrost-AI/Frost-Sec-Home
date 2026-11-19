# Maintenance — drift watchlist

OS vendors change tools, names, and support windows. Every item below is a
known drift source. Re-verify each one at every release and record a receipt
in VERIFICATION.md. Facts verified at plan time (2026-11-18) are marked.

## Windows

| Item | Status at 2026-11-18 | What to re-check |
|---|---|---|
| Windows 10 support | Mainstream support ended **2025-10-14** (verified, Microsoft) | Any further extension announcements |
| Windows 10 consumer ESU | End date **2026-10-13 has passed** (verified, Microsoft) | Whether Microsoft extended ESU again; packs default to "no more security updates — upgrade" until a new receipt exists |
| MSRT (KB890830) | Still released monthly; v5.142 seen 2026-06 (verified, Microsoft Update Catalog) | Continued monthly releases; download page validity |
| Defender cmdlets | `Get-MpComputerStatus`, `Start-MpScan`, `Get-MpThreatDetection`, `Remove-MpThreat` (no per-threat parameter), `Start-MpWDOScan` (immediate reboot) | Cmdlet availability on future Windows builds; Tamper Protection behavior |
| System Protection | Off by default on many installs; `Checkpoint-Computer` refuses >1/24h | Defaults on new builds |
| PowerShell | 5.1 built-in on Win10/11 | Any shift to PowerShell 7-only cmdlets |

## macOS

| Item | Status at 2026-11-18 | What to re-check |
|---|---|---|
| Support window | Apple supports roughly the last 3 major versions; Ventura 13 / Sonoma 14 at or past the edge by late 2026 | Exact current support list each release; EOL-warning branch in packs |
| macOS 26 (Tahoe) | Shipping with redesigned System Settings | Exact pane names/paths for every guided GUI step, per version branch |
| MRT.app | **Removed** on Ventura 13+; replaced by XProtect Remediator | Do not reintroduce MRT.app checks |
| airport CLI | Removed in Sonoma 14.4 | Never pin it |
| SSID reads | `networksetup -getairportnetwork` redacts SSID without Location permission on Sonoma+ | Keep guided Settings read as the pinned path |
| Login items | SMAppService background items not visible to osascript reads | Keep guided Settings path |
| `profiles` verb | `list` vs `show` and root requirement vary by version | Verify per version at receipt time |
| launchctl | `unload` legacy; `bootout` syntax fragile for small models | Keep quarantine-move + restart pattern |

## Linux

| Item | Status at 2026-11-18 | What to re-check |
|---|---|---|
| ClamAV freshclam | Debian/Ubuntu `apt install clamav` auto-starts `clamav-freshclam` daemon → manual `freshclam` lock-errors | Daemon behavior per distro/version; keep `systemctl is-active` pre-check |
| `dnf check-update` | Exit 100 = updates exist (not an error) | dnf5 behavior changes |
| `apt list` CLI warning | "unstable CLI" stderr warning is normal | Whether warning text changes |
| Arch `checkupdates` | Lives in pacman-contrib, often absent | Fallback must never run bare `pacman -Sy` (partial-upgrade risk) |
| rkhunter | Excluded from v1 (false positives without `--propupd`) | Reconsider only with a safe pinned workflow |
| Firewall stacks | ufw (Debian/Ubuntu), firewalld (Fedora), varies on Arch | Per-family branches stay pinned |

## Process

- Every release: walk this table, run the read-only checks on real systems,
  update VERIFICATION.md rows, and only then remove UNTESTED banners.
- New drift discovered in the wild → add a row here first, fix packs second.
- Pack `os_versions` frontmatter and GUI pane branches must be updated in the
  same commit as any verification change.
