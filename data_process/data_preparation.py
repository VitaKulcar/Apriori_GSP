import pandas as pd


def data_cleaning(dataset_name, columns_drop):
    df = pd.read_csv(f'datasets/raw/{dataset_name}.csv')

    # odstranitev praznih in odvečnih vrstic
    df.dropna(inplace=True)
    df = df.drop(columns_drop, axis=1)

    # sprememba stringa v datum
    df['DAT_OD'] = pd.to_datetime(df['DAT_OD'], format='%d.%m.%Y', errors='coerce')
    df['DAT_DO'] = pd.to_datetime(df['DAT_DO'], format='%d.%m.%Y', errors='coerce')
    df['VNOS'] = pd.to_datetime(df['VNOS'], format='%d.%m.%Y', errors='coerce')

    # omejitev na podatke od 2020-10-01 do 2021-10-01 (obdobje 1 leta)
    df = df[(df['VNOS'] >= '2020-10-01') & (df['VNOS'] < '2021-10-01')]

    # dodan stolpec trajanje
    df['TRAJANJE'] = (df['DAT_DO'] - df['DAT_OD'])

    # odstranitev negativnih dni trajanja (napake pri vnosu)
    df = df[df['TRAJANJE'] >= pd.Timedelta(0)]

    # dodajanje stolpca LETO_MESEC_VNOSA
    # df['LETO_MESEC_VNOSA'] = df['VNOS'].dt.to_period('M')
    df['LETO_TEDEN_VNOSA'] = df['VNOS'].dt.isocalendar().year.astype(str) + '_' + df['VNOS'].dt.isocalendar().week.astype(str)

    # diskretizacija števila učencev (oddelki)
    if dataset_name == 'oddelki':
        df['STEV_UCENCEV'] = pd.cut(df['STEV_UCENCEV'], bins=3, labels=['malo', 'srednje', 'veliko'])

    # diskretizacija trajanja okužbe
    df['TRAJANJE'] = pd.cut(df['TRAJANJE'], bins=3, labels=['kratko', 'srednje', 'dolgo'])

    # posplošitev zapisov regij
    """region_groups = {
        'Podravska': 'Eastern Slovenia',
        'Savinjska': 'Eastern Slovenia',
        'Pomurska': 'Eastern Slovenia',
        'Koroška': 'Eastern Slovenia',
        'Posavska': 'Eastern Slovenia',
        'Zasavska': 'Eastern Slovenia',
        'Jugovzhodna Slovenija': 'Eastern Slovenia',
        'Osrednjeslovenska': 'Central Slovenia',
        'Obalno-kraška': 'Western Slovenia',
        'Gorenjska': 'Western Slovenia',
        'Goriška': 'Western Slovenia',
        'Primorsko-notranjska': 'Western Slovenia'
    }
    df['REGIJA'] = df['REGIJA'].map(region_groups)"""

    # posplošitev zapisov
    if dataset_name != 'zaposleni':
        df.loc[df['OBDOBJE'].str.contains('razred', case=False, na=False), 'OBDOBJE'] = 'OSNOVNA ŠOLA'
        df.loc[df['OBDOBJE'].str.contains('letnik', case=False, na=False), 'OBDOBJE'] = 'SREDNJA ŠOLA'
        df.loc[df['OBDOBJE'].str.contains('star. obd', case=False, na=False), 'OBDOBJE'] = 'VRTEC'
        df.loc[df['OBDOBJE'].str.contains('stopnja', case=False, na=False), 'OBDOBJE'] = 'OSTALO'
        df.loc[df['OBDOBJE'].str.contains('skupina', case=False, na=False), 'OBDOBJE'] = 'OSTALO'
        df = df[df['OBDOBJE'] != 'OSTALO']

        terms = [
            'Klarinet', 'Kitara', 'Petje', 'Flavta', 'Pozavna', 'Rog', 'Tolkala', 'Trobenta', 'Viola',
            'Nauk o glasbi', 'Fagot', 'Tamburica', 'Klavir', 'Saksofon', 'Violina', 'Kontrabas', 'Harmonika',
            'Plesna pripravnica', 'Sodobni ples', 'Violončelo', 'Kljunasta flavta', 'Tuba', 'Oboa',
            'Predšolska glasbena vzgoja', 'Diatonična harmonika', 'Citre', 'Orgle', 'Harfa', 'Balet',
            'Glasbena pripravnica', 'Druga konična trobila'
        ]
        pattern = '|'.join(terms)
        df.loc[df['OBDOBJE'].str.contains(pattern, case=False, na=False), 'OBDOBJE'] = 'GLASBENA ŠOLA'

    """if dataset_name == 'oddelki':
        terms = [
            'Okužba s Covid-19 pri otroku ali več otrocih skupine',
            'Okužba s Covid-19 pri učencu ali več učencih oddelka',
            'Okužba s Covid-19 pri dijaku ali več dijakih oddelka',
            'Okužba s Covid-19 pri otroku / učencu / dijaku ali več učencih oddelka'
        ]
        pattern = '|'.join(terms)
        df.loc[df['VZROK'].str.contains(pattern, case=False, na=False), 'VZROK'] = 'Okužba pri otroku / učencu / dijaku'

        terms = [
            'Okužba s Covid-19 pri vzgojitelju',
            'Okužba s Covid-19 pri učitelju',
            'Okužba s Covid-19 pri predavatelju',
            'Okužba s Covid-19 pri drugem strokovnem delavcu',
            'Okužba s Covid-19 pri drugem delavcu'
        ]
        pattern = '|'.join(terms)
        df.loc[df['VZROK'].str.contains(pattern, case=False, na=False), 'VZROK'] = 'Okužba pri zaposlenem'

        terms = [
            'Sum na okužbo s Covid-19 pri otroku ali več otrocih skupine',
            'Sum na okužbo s Covid-19 pri učencu ali več učencih oddelka',
            'Sum na okužbo s Covid-19 pri dijaku ali več dijakih oddelka',
            'Sum na okužbo s Covid-19 pri otroku / učencu / dijaku ali več učencih oddelka'
        ]
        pattern = '|'.join(terms)
        df.loc[df['VZROK'].str.contains(pattern, case=False,
                                        na=False), 'VZROK'] = 'Sum na okužbo pri otroku / učencu / dijaku'

        terms = [
            'Sum na okužbo s Covid-19 pri vzgojitelju',
            'Sum na okužbo s Covid-19 pri učitelju',
            'Sum na okužbo s Covid-19 pri predavatelju',
            'Sum na okužbo s Covid-19 pri drugem strokovnem delavcu',
            'Sum na okužbo s Covid-19 pri drugem delavcu',
            'Okužba s Covid-19 pri slušatelju ali več slušateljih oddelka'
        ]
        pattern = '|'.join(terms)
        df.loc[df['VZROK'].str.contains(pattern, case=False,
                                        na=False), 'VZROK'] = 'Sum na okužbo pri zaposlenem'

        df = df[df['VZROK'] != 'Starši zavračajo izvajanje ukrepov']"""

    # odstranitev praznih vrstic
    df.dropna(inplace=True)

    # odstranitev podvojenih vrstic
    df.drop_duplicates(inplace=True)

    # ureditev podatkov po stolpcu VNOS
    df = df.sort_values(by='VNOS', ascending=True)

    # shranjevanje prečiščenih podatkov
    df.to_csv(f'datasets/cleaned_data/{dataset_name}.csv', index=False)


def group_data(dataset_name, attributes):
    df = pd.read_csv(f'datasets/cleaned_data/{dataset_name}.csv')
    grouped = df.groupby('LETO_TEDEN_VNOSA')
    for group_name, data in grouped:
        unique_data = data[attributes].drop_duplicates()
        unique_data.to_csv(f'datasets/cleaned_data/{dataset_name}/{group_name}.csv', index=False)


def generate_sequences(dataset_name, group_name):
    df = pd.read_csv(f'datasets/cleaned_data/{dataset_name}/{group_name}.csv')

    sequences = {}
    for _, row in df.iterrows():
        sequence_item = tuple(row)
        if row['REGIJA'] not in sequences:
            sequences[row['REGIJA']] = []
        sequences[row['REGIJA']].append(sequence_item)

    consolidated_sequences = []
    for region, data in sequences.items():
        consolidated_sequences.append(data)

    return consolidated_sequences
