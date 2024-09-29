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

    # dodan stolpec trajanje
    df['TRAJANJE'] = (df['DAT_DO'] - df['DAT_OD'])

    # odstranitev negativnih dni trajanja (napake pri vnosu)
    df = df[df['TRAJANJE'] >= pd.Timedelta(0)]

    # dodajanje stolpca LETO_MESEC_VNOSA
    df['LETO_MESEC_VNOSA'] = df['VNOS'].dt.to_period('M')

    # diskretizacija števila učencev (oddelki)
    if dataset_name == 'oddelki':
        df['STEV_UCENCEV'] = pd.cut(df['STEV_UCENCEV'], bins=3, labels=['malo', 'srednje', 'veliko'])

    # diskretizacija trajanja okužbe
    df['TRAJANJE'] = pd.cut(df['TRAJANJE'], bins=3, labels=['kratko', 'srednje', 'dolgo'])

    # posplošitev zapisov
    if dataset_name != 'zaposleni':
        df.loc[df['OBDOBJE'].str.contains('razred', case=False, na=False), 'OBDOBJE'] = 'OSNOVNA ŠOLA'
        df.loc[df['OBDOBJE'].str.contains('letnik', case=False, na=False), 'OBDOBJE'] = 'SREDNJA ŠOLA'
        df.loc[df['OBDOBJE'].str.contains('star. obd', case=False, na=False), 'OBDOBJE'] = 'VRTEC'

    # posplošitev zapisov
    terms = [
        'Klarinet', 'Kitara', 'Petje', 'Flavta', 'Pozavna', 'Rog', 'Tolkala', 'Trobenta',
        'Klavir', 'Saksofon', 'Violina', 'Kontrabas', 'Harmonika', 'Glasbena pripravnica',
        'Plesna pripravnica', 'Sodobni ples', 'Violončelo', 'Kljunasta flavta',
        'Predšolska glasbena vzgoja', 'Diatonična harmonika', 'Citre', 'Orgle', 'Harfa'
    ]
    pattern = '|'.join(terms)
    if dataset_name != 'zaposleni':
        df.loc[df['OBDOBJE'].str.contains(pattern, case=False, na=False), 'OBDOBJE'] = 'GLASBENA ŠOLA'

    # posplošitev zapisov ...

    # odstranitev praznih vrstic
    df.dropna(inplace=True)

    # odstranitev podvojenih vrstic
    df.drop_duplicates(inplace=True)

    # ureditev podatkov po stolpcu VNOS
    df = df.sort_values(by='VNOS', ascending=True)

    # shranjevanje prečiščenih podatkov
    df.to_csv(f'datasets/cleaned_data/{dataset_name}.csv', index=False)


def attributes(dataset_name):
    df = pd.read_csv(f'datasets/cleaned_data/{dataset_name}.csv')

    attributes_list = []
    # v vsakem stolpcu poiščemo unikatne vrednosti
    for column in df.columns:
        unique_values = df[column].unique()
        unique_values_str = ', '.join(map(str, unique_values))
        attributes_list.append({'Feature': column, 'Attributes': unique_values_str})

    attributes_df = pd.DataFrame(attributes_list)
    attributes_df.to_csv(f'datasets/attributes/{dataset_name}.csv', index=False)


def group_data(dataset_name, attributes):
    df = pd.read_csv(f'datasets/cleaned_data/{dataset_name}.csv')
    grouped = df.groupby('LETO_MESEC_VNOSA')
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
