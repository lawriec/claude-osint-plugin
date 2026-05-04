# Radio & Signals Intelligence Reference

Techniques for identifying radio signals, looking up transmitters, monitoring broadcasts, and using spectrum data for OSINT investigations. Load this reference when an investigation involves radio communications, broadcast identification, amateur radio operators, satellite tracking, or signal analysis.

---

## Software Defined Radio (SDR) Fundamentals

### What is SDR?

A Software Defined Radio replaces traditional analog radio hardware with software processing. An SDR receiver captures a wide swath of radio spectrum and processes it digitally, allowing reception of almost any signal type with the right software.

### Common SDR Hardware

| Device | Frequency Range | Cost | Notes |
|--------|----------------|------|-------|
| **RTL-SDR (v3/v4)** | 24 MHz - 1.766 GHz | ~$30 | Entry-level. Based on TV tuner chip. Receive-only. Excellent for ADS-B, FM, amateur |
| **Airspy Mini** | 24 MHz - 1.8 GHz | ~$100 | Better sensitivity and dynamic range than RTL-SDR |
| **Airspy HF+ Discovery** | 0.5 kHz - 31 MHz, 60-260 MHz | ~$170 | Excellent HF performance for shortwave monitoring |
| **HackRF One** | 1 MHz - 6 GHz | ~$300 | Transmit and receive. Wide range. Lower sensitivity than dedicated receivers |
| **SDRplay RSPdx** | 1 kHz - 2 GHz | ~$250 | Wide frequency range, good HF performance |

### SDR Software

| Software | Platform | URL | Purpose |
|----------|----------|-----|---------|
| **SDR#** | Windows | airspy.com/download | Most popular general-purpose SDR application |
| **GQRX** | Linux, macOS | gqrx.dk | Open-source SDR receiver |
| **SDR++** | Cross-platform | github.com/AlexandreRouworx/SDRPlusPlus | Modern, modular SDR application |
| **CubicSDR** | Cross-platform | cubicsdr.com | Cross-platform waterfall SDR |
| **GNU Radio** | Linux, macOS | gnuradio.org | Advanced signal processing framework for custom demodulation |

---

## Online SDR Receivers

No hardware needed -- listen to radio signals through web-based receivers worldwide:

| Platform | URL | Coverage | Notes |
|----------|-----|----------|-------|
| **WebSDR** | websdr.org | Global (100+ receivers) | HF, VHF, UHF receivers. Real-time tuning via browser. Each receiver covers its local area |
| **KiwiSDR** | rx.linkfanel.net | Global (600+ receivers) | 0-30 MHz coverage per receiver. Map-based selection. Excellent for HF monitoring |
| **Broadcastify** | broadcastify.com | Primarily US | Police, fire, EMS, aviation scanner feeds. Streaming audio |
| **LiveATC** | liveatc.net | Global | Air traffic control audio feeds from airports worldwide |
| **OpenWebRX** | sdr.hu | Global | Open-source web SDR platform. Various receivers worldwide |

**OSINT value**: Online SDRs allow you to listen to radio transmissions from specific geographic locations without being physically present. Useful for verifying broadcast activity, monitoring frequencies of interest, and geolocating signals by comparing reception across multiple receivers.

---

## Amateur Radio (Ham Radio)

### Callsign Lookup

Amateur radio operators are licensed and their callsigns are public record:

| Database | URL | Coverage | Auth |
|----------|-----|----------|------|
| **QRZ.com** | qrz.com | Global | Free basic lookup; account for full details |
| **Callsign.info** | callsign.info | Global | Free, aggregates multiple databases |
| **FCC ULS** | wireless2.fcc.gov/UlsApp/UlsSearch/searchLicense.jsp | United States | Official FCC license database. Name, address, license class, grant date |
| **ARRL Lookup** | arrl.org/advanced-search | United States | ARRL member search |
| **RAC** | apc-cap.ic.gc.ca/pls/apc_anon/query_amat_cs$.startup | Canada | Industry Canada amateur radio database |
| **Ofcom** | ofcom.org.uk/manage-your-licence/radiocommunication-licences/amateur-radio | United Kingdom | UK amateur radio licensing |
| **HamCall** | hamcall.net | Global | Aggregated international callsign database |

### Callsign Structure

Callsign prefixes are assigned by country per ITU allocation:

| Prefix | Country | Example |
|--------|---------|---------|
| W, K, N, AA-AL | United States | W1AW, K3LR, N1MM |
| VE, VA | Canada | VE3XYZ |
| G, M, 2E | United Kingdom | G3ABC, M0XYZ |
| DL, DA-DR | Germany | DL1ABC |
| F | France | F5ABC |
| JA, JH, JR | Japan | JA1ABC |
| VK | Australia | VK2ABC |
| UA-UI | Russia | UA3ABC |

The number following the prefix often indicates the geographic district within the country (e.g., W1=New England, W6=California).

### OSINT Value of Ham Radio Data

- **FCC ULS** provides full name and mailing address of US licensees
- License class reveals technical capability (Technician, General, Extra)
- Previous callsigns reveal name changes or relocations
- QRZ.com profiles often include personal details, photos, location coordinates, equipment lists
- QSL card exchanges and logbook entries reveal contacts and activity patterns

---

## Broadcast Identification

### Shortwave and HF Broadcasting

| Resource | URL | Purpose |
|----------|-----|---------|
| **HFCC** (High Frequency Coordination Conference) | hfcc.org | Official international shortwave broadcast schedules. Seasonal (A/B schedule changes) |
| **EiBi Frequency List** | eibispace.de | Comprehensive shortwave frequency database. Includes clandestine and utility stations |
| **Short-wave.info** | short-wave.info | Real-time propagation-aware schedule lookup |
| **WRTH** (World Radio TV Handbook) | wrth.com | Annual reference book. The definitive broadcast station database |
| **SWLing Post** | swling.com | Shortwave listening community and news |

### FM/AM Broadcast Lookup

| Resource | URL | Coverage |
|----------|-----|----------|
| **Radio-Locator** | radio-locator.com | US/Canada AM/FM station database with coverage maps |
| **FCC AM/FM Query** | fcc.gov/media/radio/am-fm-radio-station-search | Official US broadcast station database |
| **FMLIST** | fmlist.org | European FM station database with DX reception reports |
| **MW List** | mwlist.org | Worldwide medium wave (AM) station list |

---

## Signal Identification

### SigIdWiki

**sigidwiki.com** -- The definitive signal identification resource:
- Audio samples and waterfall images for hundreds of signal types
- Organized by frequency range, modulation type, and purpose
- Community-maintained with regular additions
- Search by frequency, name, or browse by category

### Common Signal Categories

| Category | Examples | Frequency Range |
|----------|----------|-----------------|
| **Aviation** | ADS-B, ACARS, VHF voice | 108-137 MHz, 1090 MHz |
| **Maritime** | AIS, marine VHF, NAVTEX | 156-174 MHz, 162 MHz |
| **Weather** | NOAA APT/HRPT, radiosondes | 137 MHz, 400-406 MHz, 1694 MHz |
| **Amateur** | SSB voice, CW (Morse), digital modes (FT8, RTTY) | HF bands (3.5-30 MHz), VHF/UHF |
| **Military** | STANAG 4285, HFGCS, Link-11/16 | Various HF and UHF |
| **Utility** | Time signals (WWV/WWVH), VOLMET, number stations | Various |
| **Satellite** | GPS, Iridium, GOES, Meteor-M | L-band (1.2-1.7 GHz), various |
| **Pager** | POCSAG, FLEX | 148-170 MHz, 929-932 MHz |

### Signal Identification Workflow

1. Note the **frequency** and **time** of observation
2. Record or screenshot the **waterfall display** (frequency vs. time visualization)
3. Identify the **bandwidth** (narrow = voice/data, wide = broadcast/video)
4. Identify the **modulation** (AM, FM, SSB, digital pattern)
5. Search **sigidwiki.com** with frequency and visual characteristics
6. Cross-reference with **frequency allocation tables** for the country of reception
7. Check **EiBi** or **HFCC** schedules if it appears to be a broadcast station

---

## Satellite Tracking

| Platform | URL | Purpose |
|----------|-----|---------|
| **N2YO** | n2yo.com | Real-time satellite tracking, pass predictions, footprint maps |
| **Heavens-Above** | heavens-above.com | Satellite pass predictions, ISS tracking, Starlink visibility |
| **CelesTrak** | celestrak.org | TLE (Two-Line Element) databases for orbit computation |
| **SatNOGS** | network.satnogs.org | Open-source satellite observation network. Community reception data |
| **In-The-Sky** | in-the-sky.org | Satellite visibility predictions and astronomical observations |

**TLE (Two-Line Element Sets)**: Standard format describing satellite orbits. Published by NORAD/18th Space Defense Squadron. Used by tracking software to predict satellite positions.

---

## Number Stations

Number stations are shortwave radio broadcasts of coded messages, historically associated with intelligence agencies:

| Resource | URL | Purpose |
|----------|-----|---------|
| **Priyom.org** | priyom.org | Active monitoring and scheduling of number stations. Live logs and recordings |
| **The Conet Project** | archive.org/details/irdial-disc | Historical recordings archive of number stations (Irdial-Discs) |
| **Enigma 2000** | (mailing list) | Number station identification and classification community |

Number stations are identified by designators (e.g., E11 = English-language station, S06 = Slavic-language station, M01 = Morse code station). Activity patterns can indicate geopolitical events.

---

## OSINT Applications

### Geolocating Transmitters

Radio signals can be geolocated through:
- **Triangulation**: Receiving the same signal on multiple geographically separated SDRs (e.g., KiwiSDR network) and comparing signal strength or time-of-arrival
- **Direction finding**: Using directional antennas to determine bearing to a transmitter
- **Propagation analysis**: HF signals propagate via ionospheric skip; reception patterns combined with propagation models can estimate transmitter location
- **Power/antenna analysis**: Signal strength at a known distance, combined with antenna characteristics, constrains the transmitter location

### Monitoring Emergency and Government Frequencies

- **Air traffic control**: LiveATC.net provides global coverage
- **Maritime**: AIS data is covered in `vehicle-object-id.md`; VHF channel 16 (156.8 MHz) is the international distress frequency
- **Military HF**: HFGCS (High Frequency Global Communications System) on known frequencies (e.g., 8992 kHz, 11175 kHz)
- **Emergency services**: Broadcastify for US scanner feeds; local frequency databases

### Cross-Reference with Other OSINT

- **ADS-B aircraft tracking**: Covered in `vehicle-object-id.md`. Use `uv run query_flightradar.py` for aircraft lookups
- **AIS vessel tracking**: Covered in `vehicle-object-id.md`. Use `uv run query_ais.py` for vessel lookups
- **Amateur radio operator lookup**: Callsign -> name -> full people investigation (see `people-social-media.md`)

---

## Legal Considerations

| Activity | Legality |
|----------|----------|
| **Receiving radio signals** | Generally legal in most jurisdictions. In the US, the Communications Act permits reception of any radio signal |
| **Sharing intercepted content** | Legal restrictions vary. In the US, intercepted content from certain services (cellular, encrypted) may not be divulged |
| **Transmitting** | Requires a license for most frequencies. Unlicensed transmission is illegal and can interfere with critical services |
| **Jamming signals** | Illegal in virtually all jurisdictions. Severe penalties |
| **Decoding encrypted signals** | Legal grey area. Receiving and recording is generally fine; active decryption may violate wiretapping laws |
| **Using online SDRs** | Legal. You are receiving publicly broadcast signals through a third party's receiver |

**Best practice**: Stick to passive reception and publicly available data. Document your methodology. Do not transmit, jam, or attempt to decrypt private communications.

---

## Cross-References

- `vehicle-object-id.md` -- ADS-B aircraft tracking and AIS vessel tracking
- `people-social-media.md` -- Investigating amateur radio operators via callsign lookups
- `geolocation.md` -- Using signal data to narrow geographic areas
- `opsec-ethics.md` -- Ethical guidelines for monitoring and surveillance
- `tool-guide.md` -- Plugin tool reference for `query_flightradar.py` and `query_ais.py`
