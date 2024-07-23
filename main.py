# from data_process.process_main import process
# zagon algoritmov za izkanje pravil
# if __name__ == '__main__':
    # process()


from flask_app.app import app
# vizualizacija pravil
if __name__ == '__main__':
    app.run(debug=True)
