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
    #df = df[df['TRAJANJE'] >= 0]

    # dodajanje stolpca LETO_MESEC_VNOSA
    df['LETO_MESEC_VNOSA'] = df['VNOS'].dt.to_period('M')

    # diskretizacija števila učencev (oddelki.csv)
    if dataset_name == 'oddelki':
        df['STEV_UCENCEV'] = pd.cut(df['STEV_UCENCEV'], bins=5,
                                    labels=['zelo malo', 'malo', 'srednje', 'veliko', 'zelo veliko'])

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


def generate_sequences(dataset_name, attributes):
    df = pd.read_csv(f'datasets/cleaned_data/{dataset_name}.csv')
    grouped = df.groupby('LETO_MESEC_VNOSA')

    sequences = {}
    for group_name, group_data in grouped:
        group_sequences = {}
        for _, row in group_data.iterrows():
            sequence_item = tuple(row[attr] for attr in attributes)
            if row['REGIJA'] not in group_sequences:
                group_sequences[row['REGIJA']] = []
            group_sequences[row['REGIJA']].append(sequence_item)
        sequences[group_name] = group_sequences

    # odstranitev besedila regije
    for month, region_data in sequences.items():
        s = []
        for region, data in region_data.items():
            s.append(data)
        sequences[month] = s

    return sequences
