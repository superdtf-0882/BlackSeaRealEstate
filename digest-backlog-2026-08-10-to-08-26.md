# Black Sea Monitor — Digest Backlog: August 10 – August 26, 2026

Compiled for human review before formal data update. Digests missing for Aug 15, Aug 20, Aug 23, Aug 25 (no digest generated those days). Aug 17 was published as a combined "2026-08-16/17" digest.

**Reading note:** every digest in this window reports "RPI current value: 96". That figure is wrong — `refinery_pressure.json` has held RPI at 100 since the Jul 17 update. Root cause is a pipeline defect, not a scoring disagreement: `lib/storage.getScores()` reads only `scores.json`, so `refinery_pressure.json`, `civilian_confidence.json`, and `occupation_financial_pressure.json` are never passed into the synthesis context. The model is guessing RPI/CCI/OFP values in every Dashboard Relevance section. See work-package Step 11.

---

## August 10, 2026

### Civilian Conditions

ISW's Aug 9 assessment confirms Crimea occupation authorities announced temporary fuel sales reductions at TES and Atan stations, diesel capped at 109 rubles/litre, for the week of Aug 9–15. Occupation head Gotsanyuk said increases would follow the "next shipment" — an implicit admission of continued supply uncertainty (ISW, Aug 9). The National Resistance Center reported occupation administrations across occupied territories recruiting civilians into the Russian army by exploiting unemployment and unpaid wages, targeting drone-unit recruits with false promises of safe rear-area work [unverified — Ukrainian partisan source] (UNN, Aug 9).

### Infrastructure & Logistics

Overnight Aug 8–9 drone debris struck Novorossiysk port's oil export facilities, damaging three residential buildings and injuring one person (Reuters/Global Banking & Finance Review, Aug 9). Ukraine's USF struck an oil tanker and two dry cargo shadow fleet vessels in the Black Sea the same night (Brovdi via Kyiv Post, Aug 9). Turkey's coastguard temporarily restricted Dardanelles transit licences for Novorossiysk-bound vessels after attacks on civilian ships including two Turkish vessels struck Aug 3; two Turkish officials told Reuters passage has since continued under Montreux Convention conditions (Anewz/Reuters, Aug 9). ISW confirmed a Russian strike damaged the Mayaki bridge on the M-15 Odesa–Reni highway Aug 9, and that the Kerch Strait has been blocked by Operation MoLoChKa for 30 consecutive days (ISW, Aug 9). A Ukrainian substation strike in occupied Mariupol caused confirmed power and water outages Aug 8, with occupation head Koltsov acknowledging inability to fully restore services (ISW, Aug 9).

### Real Estate & Property Administration

Freedom House's *Freedom in the World 2026*, covered by KHPG Aug 10, rates Russian-occupied Ukrainian territory at −1/100 — lower than North Korea (3/100) — citing deliberate demographic change through Russian resettlement, forced passportization, and systematic persecution of Ukrainian and Crimean Tatar identity. Documents accelerating anonymous "treason" convictions, including two women from Berdiansk and Tokmak sentenced to 12 and 14 years for donations to the Ukrainian armed forces (KHPG, Aug 10). No new Domclick or transaction-level data.

### Refinery & Export Pressure

Novorossiysk struck by drone debris Aug 9, facility identification not disclosed (Reuters, Aug 9). DW confirmed Russian authorities reported attacks on both Novorossiysk and Gelendzhik Black Sea ports (DW, Aug 9). Ukraine struck Russian S-400 air defence infrastructure at Gelendzhik overnight Aug 8 (Brovdi via Kyiv Post, Aug 9). Turkey's temporary Dardanelles restrictions signal cumulative Black Sea interdiction pressure affecting the institutional framework governing access to Russia's primary crude export artery; 80%+ of Kazakhstan's oil exports transit the Novorossiysk CPC terminal (Anewz, Aug 9).

### Dashboard Relevance (as generated)

RPI: no change, at ceiling; flag Dardanelles restriction as watch condition. CCI: no change, at ceiling; log NRC recruitment-through-unemployment report if corroborated. **Track B Mariupol 22 → 21 suggested**, reflecting confirmed substation strike causing power/water failure in the city itself.

---

## August 11, 2026

### Civilian Conditions

ISW confirmed ongoing power outages and fuel shortages in occupied Crimea, Krymenergo reporting grid damage (ISW, Aug 9). NRC reported occupation administrators exploiting unemployment and months-long wage delays to recruit civilians into the Russian army under false pretenses [unverified — Ukrainian partisan source] (UNN/NRC, Aug 9). Freedom House rated all Russian-occupied Ukrainian territory at −1/100 (KHPG/Coynash, Aug 10).

### Infrastructure & Logistics

Drone debris from a large overnight attack fell on two unidentified facilities at Novorossiysk Aug 9 (Reuters, Aug 9). ISW confirmed the Mayaki bridge strike on the M-15 Odesa–Reni highway, assessing Russia is deliberately targeting Ukraine's alternative land grain export corridor after maritime routes were degraded (ISW, Aug 9). Turkey's coastguard reportedly began delaying or denying transit licences for Novorossiysk-bound vessels per Bloomberg sources (Anewz, Aug 9), though two Turkish officials told Reuters passage remains open under Montreux — unresolved. Brovdi reported striking an S-400 at Gelendzhik, air defence radars in Rostov Oblast, and three shadow fleet vessels overnight Aug 8; Operation MoLoChKa has now targeted 218+ vessels since Jul 6 and claims 30 days of Kerch Strait blockage (Kyiv Post, Aug 9) [unverified — Ukrainian military source].

### Real Estate & Property Administration

No new transaction data, price indices, or property administration actions beyond items already in key_events.

### Refinery & Export Pressure

Novorossiysk debris strike Aug 8–9, three residential buildings damaged, one injured (Reuters, Aug 9). Turkey's partial and contested Dardanelles restriction, if sustained, would compound export pressure on Russia's primary Black Sea crude loading terminal, already down 38% in large-ship sailings in July. ISW noted Russian strikes on Ukrainian oil facilities in Sumy's Okhtyrka district [unverified — Russian state source via ISW] and continued heavy strikes on Odesa port infrastructure (ISW, Aug 9).

### Dashboard Relevance (as generated)

No dial changes. **Track B Donetsk/Luhansk: modest downward pressure (−2 each) suggested for next cycle if corroborated** — NRC structural unemployment and unpaid wages across occupied territories. Monitor condition only.

---

## August 12, 2026

### Civilian Conditions

Sevastopolenergo announced temporary power supply restrictions Aug 11 citing "significant power shortages in the Crimean power grid" (ISW, Aug 11). Ukrainian Navy spokesperson Pletenchuk stated Aug 11 that Russia has "effectively lost Crimea as a naval base" (UATV, Aug 11).

### Infrastructure & Logistics

Overnight Aug 11–12 Ukrainian drones conducted a massive attack on Novorossiysk's naval harbour; NASA FIRMS thermal imagery confirmed fires across multiple navy piers and the adjacent Grushovaya oil depot. A probable strike on the Novorossiysk Grain Elevator — a major grain export complex — was reported, with 2 killed and 13 injured (Censor.NET, Aug 12; UNN, Aug 11; Maritime Executive, Aug 11; Kyiv Independent, Aug 12). Overnight Aug 10–11, USF struck 43 military and energy targets in occupied Crimea and southern Ukraine, including energy hubs in Berdiansk and Mariupol, a Buk-M3 system, logistics depots, an ammunition depot, and a shadow fleet dry cargo vessel (NV Ukraine/Ukrainska Pravda, Aug 11; ISW, Aug 11). The Orsk (Orsknefteorgsintez) refinery in Orenburg Oblast was struck overnight Aug 10–11 (Reuters, Aug 11). Explosions reported near Sevastopol's Balaklava Thermal Power Plant and near the Crimean Bridge overnight Aug 12; fire at a Russian military border guard post in northern Crimea (Mezha.net, Aug 12).

### Real Estate & Property Administration

A mandatory Russian school textbook series, "History of Our Region: Donbas and Novorossiya," added to the federal curriculum for grades 5–7 in occupied Donetsk, Luhansk, Zaporizhzhia and Kherson, mandatory from Sept 1, 2026 (Euromaidan Press, Aug 11; Intent Press, Aug 11). FDD/Washington Times noted a Chinese-operated crushed-stone quarry near Mariupol running on Chinese machinery under 2023-era agreements (FDD, Aug 11).

### Refinery & Export Pressure

Reuters tracker Aug 11 confirmed strikes on at least 15 major Russian refining facilities since late June: Orsknefteorgsintez (6M t/yr) Aug 11, TANECO (17M t/yr) and ZapSibNeftekhim (2.5M t/yr) Aug 10, Yaroslavl (15M t/yr), Volgograd Lukoil (13.5M t/yr, fully halted since Jul 31). S&P Global via United24: at least 26 Russian facilities knocked offline in 2026; by late July only 8 had returned to full operations, 11 partial, 7 idle. Russia importing gasoline from Belarus at record levels — rail shipments up 25-fold Jan–Jul 2026 vs 2025 — plus India, Kazakhstan and Morocco (United24, Aug 11). Black Sea drone attacks cut CPC loadings at Novorossiysk by up to a fifth in July (Reuters, Aug 11). Vance reportedly asked Ukraine not to strike non-Russian tankers near the CPC (Ukrainska Pravda/Kyiv Independent, Aug 12).

### Dashboard Relevance (as generated)

No numeric dial changes. Novorossiysk grain elevator and naval harbour strikes flagged as key_event candidates — new target category (grain export infrastructure) and confirmed naval infrastructure damage at Russia's primary BSF relocation port.

---

## August 13, 2026

### Civilian Conditions

Sevastopol grid operator announced temporary power restrictions Aug 11 following overnight strikes on Crimean energy infrastructure. Fire at a Russian border guard post in Rysove, Krasnoperekopsk District, northern Crimea, overnight Aug 12 (Crimean Wind, Aug 12). No material change in severity from the Aug 8 baseline.

### Infrastructure & Logistics

Ukraine struck the Novorossiysk naval base overnight Aug 11–12 in what Zelensky called a "unique operation," using Palianytsia drones, Neptune missiles and naval drones. Ukraine's General Staff confirmed four Russian warships damaged — Admiral Grigorovich-class frigates *Admiral Makarov* and *Admiral Essen*, one Buyan-M missile ship, one *Vasil Bykov* patrol ship — and the Novorossiysk grain terminal temporarily suspended operations (Kyiv Independent, Aug 12; Reuters, Aug 12). Brovdi confirmed strikes on energy hubs in occupied Berdiansk and Mariupol overnight Aug 10–11 as part of a 43-location operation (NV Ukraine/Ukrainska Pravda, Aug 11).

### Real Estate & Property Administration

No new developments. BBC Verify expropriation data (Aug 7) and ZMINA Jul 24 reporting on Mariupol's 13,000+ "ownerless" designations remain the most recent logged entries.

### Refinery & Export Pressure

Reuters Aug 11 tracker: Orsk (6M t/yr), ZapSibNeftekhim (2.5M t/yr), TANECO (17M t/yr), Yaroslavl (15M t/yr), Volgograd (13.5M t/yr, halted since Jul 31), Saratov (5.8M t/yr, halted Aug 2), Ryazan (13.1M t/yr, halted Jul 29), Perm (12.6M t/yr, one CDU down), Tyumen (6M t/yr, halted). Black Sea drone attacks removed up to one-fifth of CPC loadings in July. Fire at Rosneft Komsomolsk refinery Aug 11, attributed by authorities to technical failure (United24, Aug 11).

### Dashboard Relevance (as generated)

RPI at ceiling, no change. **Key_event candidates: Novorossiysk naval strike Aug 12** (largest confirmed BSF damage since campaign began) and **the mandatory "Donbas and Novorossiya" textbook, Sept 1 implementation** — a formal Russification milestone reinforcing the administered settler economy trajectory.

---

## August 14, 2026

### Civilian Conditions

Sevastopol occupation head Razvozhayev confirmed power grid damage and city-wide outages following Aug 13–14 strikes on the Balaklava TPP and multiple substations (Ukrainska Pravda, Aug 14). NPR Aug 13 reported a Russian resident describing Crimea as having "no gasoline, no fuel, no power," with stores and banks closed. The Center of National Resistance reported grain carriers refusing to enter occupied agricultural territories due to drone threat, harvested grain accumulating unsold in warehouses, agricultural enterprises pushed toward bankruptcy (Ukraine Business News, Aug 14).

### Infrastructure & Logistics

USF struck 29 energy nodes overnight Aug 13–14 under Operation "Crimean Switch Off": the Balaklava TPP in Sevastopol, multiple Mariupol 110 kV substations (Misto-3, NS-2, Illich, Misto-6), the GRS-1 Mariupol gas distribution station, and **at least seven Berdiansk substations across 150 kV and 110 kV tiers** (Ukrainska Pravda/Mezha.net/Brovdi, Aug 14). Overnight Aug 11–12 Novorossiysk naval base strike damaged frigates *Admiral Essen* and *Admiral Makarov*, a Buyan-M and patrol vessel *Vasily Bykov*, while halting three major grain terminals including KSK Kombinat Stroikomplekt (ISW/Newsweek, Aug 13). Fire at Ust-Luga port, Leningrad Oblast, overnight Aug 13–14 (Ukrainska Pravda, Aug 14).

### Real Estate & Property Administration

Russia's FSB has begun dismantling the internal border zone separating Russia from annexed Ukrainian territories in Rostov, Voronezh and Crimea, citing "completed annexation" of Donetsk, Luhansk and Kherson — despite lacking full control of any of the four claimed oblasts (Meduza/Agentstvo, Aug 13). Ukraine's CEC declared the planned Sept 20 Russian State Duma elections in occupied Donetsk, Luhansk, Zaporizhzhia, Kherson and Crimea illegitimate (UNN, Aug 13).

### Refinery & Export Pressure

Ukraine struck the Gazprom Neftekhim Salavat refinery in Bashkortostan overnight Aug 12–13 — Russia's largest Gazprom petrochemical complex at 7.5–10M t/yr — its second strike in 2026 (AP/ISW, Aug 13). The Orsk refinery confirmed full operational halt after the Aug 11 strike, with the governor stating repairs could take **up to six months** due to imported equipment and sanctions barriers (EA WorldView/ISW, Aug 13–14). Fourth Russian refinery struck in three days; campaign targeting ~42–45% of Russian refining capacity. Orenburg region introduced fuel rationing after the Orsk shutdown; more than 50 Russian regions now have some form of fuel restriction (EA WorldView, Aug 13).

### Dashboard Relevance (as generated)

RPI at ceiling. **Track B Berdiansk 12 → 10 suggested** — second confirmed round of energy infrastructure strikes on Berdiansk in the monitoring period. Track A Crimea: NPR ground-truth confirmation of complete private market collapse, no adjustment beyond the Aug 9 floor of 40 pending new price data. Agricultural logistics collapse flagged as a new CCI-relevant signal.

---

## August 16, 2026

### Civilian Conditions

Third Galaktika chain shopping centre fire in occupied Donetsk in August, reported Aug 16, with drone flyovers reported by eyewitnesses before the fire at the Kuibyshevskyi district facility; prior fires hit Makiivka Aug 9–10 and Yenakiieve Aug 14 (RBC Ukraine/ASTRA, Aug 16). Donetsk Regional Military Administration confirmed one civilian killed and six injured in Russian strikes Aug 15 (UNN, Aug 16).

### Infrastructure & Logistics

**Crude oil exports from the Sheskharis terminal at Novorossiysk were suspended Aug 14** following Aug 12 drone strikes that damaged main berths; storage tanks reached capacity with one tanker moving to sea rather than loading (NV Ukraine/Reuters, Aug 15). **The KSK grain terminal — Russia's largest Black Sea grain facility by transshipment volume, handling over 40% of Novorossiysk grain exports — halted all operations Aug 15**; all three Novorossiysk grain terminals suspended simultaneously (UA News, Aug 15). Ukraine struck the Savasleyka airbase in Nizhny Novgorod (MiG-31K Kinzhal carriers) and the Progress Rocket Space Center in Samara Aug 15 using Flamingo missiles (ISW, Aug 15). FSB drafted orders to abolish border zones between Rostov/Voronezh and occupied Donetsk/Luhansk, and between occupied Crimea and occupied Kherson (NV Ukraine/Babel, Aug 15).

### Real Estate & Property Administration

**DW investigation published Aug 14–15**: Russian contractor Su-2007 has built multiple 12–15 floor high-rise blocks (Leningradsky Kvartal complex) on cleared sites in central Mariupol, on locations where residents were killed or displaced in 2022. Apartments selling at 7.5–10 million rubles (€104,000+) under a 2% state mortgage available only to Russian citizens, minimum 2% deposit. Buyers predominantly Russian security personnel, officials and logistics workers. **Property prices in Mariupol have risen roughly one-third in one year** per economist Vyacheslav Shiryaev. **Buyers are insuring mortgages against war risks.** Original residents received no units and were relocated to city outskirts or hostels (DW, Aug 14).

### Refinery & Export Pressure

The Sheskharis suspension follows the Aug 12 Novorossiysk attack, which ISW confirmed also triggered **Russian Railways cargo loading restrictions at Novorossiysk from Aug 13–22** (ISW, Aug 15). Salavat struck Aug 13–14; Ust-Luga struck Aug 14 (Helsinki Times, Aug 15). VEB.RF chief economist Andrei Klepach publicly stated Russia is losing the economic war of attrition, that the Russian economy entered decline in 2026, and predicted an inevitable social crisis (Ukrainska Pravda/Moscow Times, Aug 16). The Times (UK) reported Aug 15 that Ukraine's deep-strike campaign has cut Russia's oil and fuel production capacity by 35% and caused over £35 billion in economic damage.

### Dashboard Relevance (as generated)

RPI: largest single-event port closure since the monitoring period began; incremental pressure real but not a structural step-change from ceiling. **Track A Mariupol: hold at 29 or +1** — settler mortgage activity is state expenditure, captured more accurately in SCI; methodology penalises near-zero genuine private entry. SCI Mariupol: hold at 91. **Track B Mariupol: hold at 22 or marginal downward** — war-risk insurance is a new qualitative indicator that buyer permanence is structurally hedged.

---

## August 17, 2026 (published as combined 2026-08-16/17)

### Summary

Sheskharis terminal suspension characterised as the most significant export disruption of the cycle, handling approximately 700,000–1,000,000 barrels daily. All three Novorossiysk grain terminals halted. Balaklava TPP in occupied Crimea reportedly ceased operations following strikes. Ukraine proposed a Black Sea civilian shipping truce, which Russia formally rejected. Cumulative Ukrainian deep strikes have reduced Russia's oil and fuel production capacity by 35%. British drone systems confirmed in deep-strike missions against Russian refineries for the first time. DW's Mariupol investigation confirms 15 high-rise buildings on destroyed Ukrainian residential sites; the 2% programme ceiling is 6 million rubles, requires Russian citizenship and a minimum 2% deposit, and functions as the primary financial instrument driving settler colonisation. Russian banks report **Mariupol leads occupied-territory mortgage volumes**.

### Dashboard Relevance (as generated)

RPI at ceiling, sustained deepening. Track A Mariupol 29: market structurally state-subsidised with administered pricing and Russian buyer demographics, no genuine private capital entry. Track B Mariupol 22: original residents received no apartments; buyers hold mortgages against war risks. CCI 100: third Galaktika fire.

---

## August 18, 2026

### Civilian Conditions

**Gasoline has again run out at most Crimea filling stations as of Aug 16, with electricity rationing and water cutoffs confirmed in 35 settlements** (intent.press, Aug 16). Occupation authorities in Crimea reportedly planning to **replace hot school meals with dry rations** (intent.press, Aug 17). No recovery has occurred since the July peak.

### Infrastructure & Logistics

Ukraine's Azov Brigade launched Operation Hell-2 Aug 17, reporting complete destruction of Russian military fuel storage and supply facilities across occupied Donetsk Oblast [unverified — Ukrainian partisan source] (NV Ukraine/United24, Aug 17). **The Greek-flagged Suezmax tanker *Skiros*, carrying Russian crude, was struck by a drone at the CPC terminal near Novorossiysk on the evening of Aug 16 — the first attack on a CPC-terminal vessel after a near-three-week lull** (Meduza/Bloomberg via Ukrainska Pravda, Aug 17–18). Sheskharis resumed crude loadings Aug 17 after the Aug 14 halt, though cumulative disruption has cut CPC shipments by roughly 600,000 bpd compared with May (Reuters, Aug 17). **Moscow Times Aug 17: more than 90% of Russia's grain export capacity in the Azov–Black Sea basin is offline** — all three Novorossiysk grain terminals, the Taman terminal, and Sea of Azov navigation all suspended, threatening $15 billion in annual Russian grain export revenue at peak harvest season.

### Real Estate & Property Administration

DW investigation amplified by Euromaidan Press and United24 (Aug 17): Russians — primarily security personnel, officials and military logistics workers — actively purchasing new Mariupol apartments built over destroyed Ukrainian homes using 2% subsidised mortgages (minimum 2% down, capped at 6 million rubles / ~$65,000). Displaced Ukrainian former residents received none of the replacement units. Occupation authorities have ordered some surviving-apartment residents out to hostels or city outskirts. Mariupol leads all Russian-occupied cities in mortgage loan volume; local housing prices up approximately one-third over the past year per Russian banking statistics.

### Refinery & Export Pressure

**VEB.RF chief economist Andrei Klepach was fired on approximately Aug 18** after publicly warning that Russia "will not win" its war of attrition, citing growing losses from Ukrainian strikes on ports, oil and gas facilities, chemical plants and logistics as a "significant macroeconomic barrier" (Firstpost, Aug 18). Ukrainian Neptune missiles struck the Kamensky Combine rocket fuel plant in Rostov Oblast overnight Aug 15–16, destroying two production workshops and damaging four others, disrupting solid rocket fuel production for Uragan, Smerch and Tornado-S (Ukrainska Pravda/Censor.NET, Aug 17).

### Dashboard Relevance (as generated)

No numeric dial changes. All significant developments either continuation of existing trends or already captured in key_events.

---

## August 19, 2026

### Civilian Conditions

Intent.press Aug 16: electricity rationed in Crimea, water cut off in 35 settlements, gasoline again out at most stations. Aug 17: occupation authorities planning to replace hot school meals with dry rations. Persistent rather than escalating.

### Infrastructure & Logistics

*Skiros* struck Aug 16 after loading Russian-origin crude at the CPC terminal, ending a nearly three-week lull in vessel strikes at that facility (Bloomberg via Meduza/Ukrainska Pravda, Aug 17–18). Sheskharis halted Aug 14, resumed Aug 17 with a Suezmax loading Kazakh KEBCO crude (Reuters, Aug 17). Moscow Times Aug 17: over 90% of Russian grain export capacity in the Azov–Black Sea basin offline. Azov Corps confirmed "Operation Hell-2" Aug 17 [unverified — Ukrainian partisan source].

### Real Estate & Property Administration

DW via Euromaidan Press and United24 (Aug 17): Russians purchasing new Mariupol apartments at 2% mortgage rates, original residents receiving nothing, some evicted from surviving units. Economist Vyacheslav Shiryaev states construction companies "save on everything" while charging high prices. Local housing prices up roughly one-third over the past year — administered settler demand, not genuine private market confidence. **Mariupol City Council confirmed it has won $34.12 million in court judgments against Russia across 16 lawsuits for destroyed municipal property, with 40 more assessments pending** (UA News, Aug 17).

### Refinery & Export Pressure

Ukraine's Navy confirmed Aug 17 that Neptune cruise missiles struck the Kamensky Combine in Rostov Oblast Aug 16 (Ukrainska Pravda/Censor.NET, Aug 17). Klepach fired after stating Russia "will not win this war of attrition" (Firstpost, Aug 18). ISW Aug 17 confirms the Azov Donetsk fuel operation as a sustained one-month campaign targeting rear logistics.

### Dashboard Relevance (as generated)

RPI: the Skiros strike confirms the Ukraine–US agreement to spare non-Russian CPC vessels did not hold for Russian-cargo vessels. Kamensky adds a new category of upstream military-industrial damage. Hold at ceiling. **Track B Crimea 26 → 25 suggested**, reflecting cumulative service degradation now reaching education provisioning; spread would widen from −23 to −24.

---

## August 21, 2026

### Civilian Conditions

**Fuel availability across Russia has fallen to just 28% of gas stations as of Aug 18**, per ISW citing Izvestia and the GdeBENZ crowd-sourced app (ISW, Aug 19). Moscow Times Aug 19: Gazprom Neft reinstated 60-litre purchase caps, Tatneft capped at 50 L gasoline / 60 L diesel, Rosneft limited gasoline to 30 L per vehicle nationally. **ISW Aug 19: Rosgvardia paramilitary units have deployed to gas stations in Moscow Oblast and at least 13 stations across Russia and occupied Crimea to manage fuel-related civil unrest.** Crimean Wind reported Aug 19 that **hotel occupancy in occupied Crimea fell roughly 35% in July and 30% in August** due to combined fuel shortages, power disruptions and logistical collapse [unverified — Ukrainian partisan source] (ISW, Aug 19).

### Infrastructure & Logistics

Ukrainian forces struck a road bridge over the Molochna River near Molochansk in occupied Zaporizhzhia, three drone depots in occupied Donetsk and Luhansk, a Geran/Gerbera drone control relay in occupied Crimea (Olenivka), and a logistics depot in Kadiivka, Luhansk Oblast, overnight Aug 18–19 (Ukrinform/Pravda, Aug 19). Footage from Aug 19 shows Russian trucks and fuel tankers burning on the M-14 Berdyansk–Mariupol highway (ISW/Censor.NET, Aug 19). **Satellite imagery analysed by Militarnyi (Aug 19) indicates both frigates *Admiral Makarov* and *Admiral Essen*, struck Aug 12, sustained damage to their 3S14 vertical launch systems and may have lost the ability to fire Kalibr missiles, with repairs likely exceeding one year.** Ukrainian strikes hit the Ufa Oil Refining Hub in Bashkortostan overnight Aug 18–19, destroying the AVT-6 primary refining unit at the Bashneft facility (ISW/CriticalThreats, Aug 19).

### Refinery & Export Pressure

**Russian oil exports from western ports fell to approximately 2.3 million bpd in the first half of August, 15% below the planned 2.7 million bpd**, driven by disruptions at Novorossiysk (Reuters, Aug 19). **Novorossiysk loadings specifically collapsed to roughly 400,000 bpd, compared with 800,000–1,000,000 bpd in June and July**, and loadings are more than two weeks behind schedule. Ukraine Business News (Aug 20): Russian seaborne crude exports fell to 3.58 million bpd in the four weeks through Aug 16, the lowest since late April and the fifth consecutive week of decline, with **zero tanker crude loadings at Novorossiysk in the week ending Aug 16**. Drone strike on oil and energy facilities in Nizhnekamsk and Krasnodar Krai Aug 20 (Mezha.net, Aug 20).

**Counter-signal:** a European intelligence source cited by Ukraine Business News noted that "elevated Urals crude prices (averaging $82/barrel in Q2) have added approximately $30 billion in export revenue," providing Putin additional fiscal runway through at least spring 2027. *Reviewer's note: this conflicts with CREA's Aug 10 monthly analysis putting July Urals at $60.22/bbl at a 26% ($21) discount to Brent, −3% MoM. CREA is the methodology's named source for this component. Treat the $82 figure as a Q2 average at best, and do not use it as an August anchor.*

### Dashboard Relevance (as generated)

RPI at ceiling, no change. CCI at ceiling; the Crimean Wind hotel occupancy data is new and specific to August 2026 and confirms the ceiling reading is not stale. **Track A Crimea 40 → 38–39 suggested**: fresh August-specific hotel data confirms the floor is holding with no upward bounce during what should be peak summer.

---

## August 22, 2026

### Civilian Conditions

**Occupied Crimea faces a deteriorating fuel quality crisis: civilian vehicles are breaking down due to mandatory use of lower-grade Euro-2 and Euro-3 gasoline, down from Euro-5**, as Russia authorised inferior fuel nationwide to compensate for reduced refinery output (ISW, Aug 21). Power shortages persist across occupied Crimea, with Krymenergo and Sevastopolenergo implementing restricted schedules (ISW, Aug 21). Russia has begun importing refined fuel, with kilometre-long gasoline queues in Moscow and purchase caps at Rosneft (30 L), Gazprom Neft (40–60 L), Tatneft (50 L) and Lukoil (Kyiv Post, Aug 21).

### Infrastructure & Logistics

**Ukrainian forces struck two cargo vessels in the Black Sea Aug 21: a naval drone hit the Barbados-flagged container ship *RMS TEAM*, forcing the crew to abandon ship, while a second drone damaged the bridge and living quarters of the Turkish-owned *VOLGO-BALT 226*** (ISW, Aug 21). Ukrainian forces also struck drone relay stations in occupied Crimea at Sterehushche and Chornomorske, a materiel warehouse in Novosilske, and a freight truck on the E-97 Armyansk–Simferopol highway (Ukrainian General Staff via ISW, Aug 21). Russian forces struck the Ukraine–Moldova border crossing at Tabaky in Odesa Oblast for the second consecutive night.

### Refinery & Export Pressure

Ukraine struck the Lukoil Permnefteorgsintez refinery in Perm overnight Aug 20–21, geolocated footage confirming a fire at a tank farm or phenolic oil purification unit (ISW, Aug 21). **Leaked communications from Moscow Deputy Mayor Gorbenko's office show officials privately acknowledging Russia cannot defend Moscow's refineries and proposing decentralised mini-refinery networks** (ISW, Aug 21). An Oman-flagged tanker carrying ~68,000 metric tons of Indian-origin gasoline unloaded at Russia's Arctic port of Vitino, with additional Indian cargoes and rail imports from Belarus and Kazakhstan en route (Kyiv Post, Aug 21).

### Dashboard Relevance (as generated)

CCI at ceiling, no adjustment. RPI: suggested upward from "96" toward 97–98 (*note: RPI is already 100 in the data file — see reading note at top*). Track B Crimea 26: conditions worsen at margins, no update warranted this cycle.

---

## August 24, 2026

### Civilian Conditions

Russian forces restricted entry to occupied Kakhovka Aug 24, turning back people seeking goods (Mezha.net, Aug 24). No new fuel or food data beyond what is already in key_events.

### Infrastructure & Logistics

USF struck three Ozon logistics centres overnight Aug 23–24 — Krasnodar, Adygea (Enem), Stavropol Krai (Nevinnomyssk) and Dagestan (Tyube) — the third consecutive night of strikes on the retailer; a radar tracking unit in occupied Crimea caught fire after four strikes (Kyiv Post/Kyiv Independent, Aug 24). **ISW Aug 23 confirms Ukrainian forces struck 27 power plants across occupied southern Ukraine and Crimea between Aug 17–22 (267 total since Aug 1) and 36 vessels in the Azov and Black Seas in the same period, with electrical substations struck near occupied Berdyansk during that window** (ISW, Aug 23).

### Real Estate & Property Administration

No new developments. Russia's use of the rebuilt Mariupol Drama Theater as a propaganda film set (United24/UATV, Aug 24) confirms ongoing occupation-narrative operations at rebuilt sites.

### Refinery & Export Pressure

Independence Day drone campaign extended to a second Ozon hub in Orenburg, a Kuchenland facility in Krasnodar, and confirmed shadow fleet tanker and bulk carrier strikes in the Black Sea (Ukrainska Pravda, Aug 24). **ISW confirms the Aug 17–22 window included a 500 kV Taman electrical substation in Krasnodar Krai — a key node for Crimea power transfer — and the Kurskaya substation in Kursk Oblast** (ISW, Aug 23). **Putin publicly acknowledged the strike campaign as opening "Pandora's box" and threatened retaliation against Ukraine's "most sensitive economic sectors"** (Taipei Times/AFP, Aug 24; Reuters, Aug 23).

### Dashboard Relevance (as generated)

RPI at ceiling; "the index cannot register additional upward movement until the methodology is recalibrated or a structurally new target category emerges." CCI at ceiling; Kakhovka access denial flagged. **Track B Berdiansk 12 → 11 suggested** if no recovery data emerges.

---

## August 26, 2026

### Civilian Conditions

**ATESH reported Aug 26 that Russian military commanders from the 70th Motorized Rifle Division are selling military fuel allocations to civilians in Donetsk, Luhansk and Rostov-on-Don at prices starting at 300 rubles per litre**, leaving the unit with acute fuel shortages affecting armoured operations and casualty evacuation [unverified — Ukrainian partisan source] (Ukrinform, Aug 26). Explosions across occupied Crimea accompanied by power outages Aug 26 (mezha.net, Aug 26). Inflation surging in occupied Crimea with fuel prices described as having more than tripled (mezha.net, Aug 25).

### Infrastructure & Logistics

**Ukrainian drones struck the Lukoil NORSI refinery in Kstovo (Nizhny Novgorod Oblast) overnight Aug 25–26 — Russia's fourth-largest refinery and second-largest gasoline producer** (Kyiv Post/Ukrainska Pravda, Aug 26). A simultaneous strike hit a Wildberries logistics hub in Kotovsk (Tambov Oblast), causing a fire covering over 100,000 m² and halting deliveries; Ukrainian defence company Fire Point confirmed its FP-1 drones executed both strikes in a single night (Kyiv Post, Aug 26). Ukraine's General Staff reported strikes Aug 24–25 against fuel, ammunition and logistics depots in **Berdiansk and Prymorsk** (Zaporizhzhia Oblast), Russian EW systems in Luhansk and in the Crimean village of Myrnyi, and damage to a MiG-29 at Millerovo airfield (Ukrainska Pravda, Aug 25). Russian military truck convoys from Mariupol toward Huliaipole observed for a third consecutive day Aug 25 [unverified — Ukrainian partisan source] (UA News, Aug 25).

### Real Estate & Property Administration

**A legal analysis published Aug 26 on EJIL:Talk by Veronika Vozniuk documents Russia's settlement incentive framework across occupied Donetsk, Luhansk, Zaporizhzhia and Kherson: the 2%-mortgage programme (active until 2030) had issued more than 6,000 loans as of late 2025; Federal Constitutional Law No. 4-FKZ (December 2025) enables redistribution of confiscated Ukrainian properties to Russian citizens; and official territorial planning documents project an additional 113,800 residents in occupied territories by 2045** (EJIL:Talk, Aug 26). GUR is cited as documenting approximately 200,000 ethnic Russians in occupied Donetsk, Luhansk, Zaporizhzhia and Kherson, with a further 200,000–300,000 in occupied Crimea as of July 2026.

### Refinery & Export Pressure

**Bloomberg Aug 25: Russian seaborne crude exports fell to 3.46 million bpd in the four weeks to Aug 23 — the lowest in four months** — as drone strikes on oil tankers cut Black Sea shipments. Moscow has been forced to redirect Kazakh crude to Novorossiysk to free Baltic Ust-Luga capacity for Russian barrels. **Russian oil output fell to 8.89 million bpd in July — the lowest in six years and nearly 1 million bpd below its OPEC+ quota.** Four-week average gross export value $1.65 billion weekly, down $80 million from the prior period. Ukraine has now struck Russian refineries on what Bloomberg describes as "an almost nightly occurrence." **Putin signed a decree Aug 25 authorising temporary state seizure of critical infrastructure — including energy, fuel and logistics facilities — from private owners who fail to protect or repair them after drone strikes**; analysts noted owners are reluctant to invest in repairs given repeated targeting (AP/ABC News, Aug 25).

### Dashboard Relevance (as generated)

RPI: no change, at or near ceiling. **CCI: the ATESH fuel-diversion report is a new data point indicating military fuel is now flowing into civilian grey markets in the occupied Donbas cities themselves — directionally upward for Donetsk and Luhansk, which have not previously had confirmed acute fuel access failures at Crimea intensity. Suggested +3 to +5 in the next cycle if corroborated by a second source.** SCI Mariupol 91: EJIL:Talk confirms 6,000+ mortgages with continued growth, not new enough to change the reading.

---

## Corroboration performed outside the digest pipeline

These figures were verified directly against primary reporting during work-package preparation, because they carry the weight of this cycle's OFP decision:

- **Minfin / federal budget, Jan–Jul 2026** (published Aug 12): deficit **6.5 trillion rubles ($78.9bn), 2.8% of GDP**, against a full-year target of 3.8 trillion rubles (1.6% of GDP) — **1.7× the annual target with five months to run**. Revenue 22.1T, spending 28.6T, spending +14.5% YoY. Planned annual spending revised 44.1T → 45.1T, pushing the projected full-year deficit toward ~4.8T. Finance Ministry has not disclosed a detailed federal spending breakdown since May 2022. (Interfax/NV, Aug 12)
- **CREA monthly analysis, July 2026** (published Aug 10): total fossil fuel export revenue **€683M/day, −12% MoM**. Crude oil €392M/day (+1% MoM; pipeline −21%, seaborne +7%). **Urals average $60.22/bbl, −3% MoM, at a 26% ($21) discount to Brent.** Oil product export revenue **€116M/day, −45% MoM**. **Oil product loadings 4.7 million tonnes, −23% MoM — lowest on record, and less than half the 9.6Mt of July 2025.** Tuapse loaded almost no products for a second consecutive month.
- **Bloomberg, Aug 25**: seaborne crude 3.46M bpd four-week average to Aug 23 (four-month low); 33 tankers loaded 24.79M barrels in the week to Aug 23; four-week gross export value $1.65bn/week, −$80M; crude output 8.89M bpd, ~1M bpd below OPEC+ quota; Novorossiysk loadings "well below normal" after resuming.
- **Putin infrastructure decree, signed Aug 25**: authorises temporary state control of critical infrastructure — energy, industry, communications, transport, logistics — where private owners fail to protect or rebuild after attacks. Deputy PM Manturov framed it as "involvement of the state in the management of an enterprise to solve specific security problems," not permanent nationalisation, with decisions "at the highest level." Peskov: "often business owners do not pay enough attention to taking measures to ensure safety, anti-drone safety." Analyst Abbas Gallyamov characterised it as an ultimatum to refinery owners: "If you don't finance the restoration of the refineries, we'll take them away from you." (AP/ABC, CNN, Washington Post, Aug 25)
- **NWF**: no new Minfin disclosure in this window. The Aug 6 release (Aug 1 data) remains the current anchor; the next monthly disclosure is expected ~Sept 3. The NWF component of OFP therefore has no new data this cycle and should not move.
- **Graham sanctions bill**: passed the Senate Aug 7 and is with the House. No House vote in this window. Remains a watch condition.

---

*Compiled 2026-08-26 for the Aug 26 scoring cycle. Digests retrieved from https://black-sea-real-estate.vercel.app/api/digest/*
