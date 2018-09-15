import os
import shutil
import re
import random
from model import ModelClass

INPUT_PATH = './input_files/'
OUTPUT_PATH = './output_files/'
TEMP_FILE_FOLDER_PATH = './tmp/'
NUMBER_OF_WORDS_IN_TMP_FILE = 1000


def load_model():
    model = ModelClass()
    return model


def load_input_files_list():
    return os.listdir(INPUT_PATH)


def clear_tmp():
    files_path = os.listdir(TEMP_FILE_FOLDER_PATH)
    for file_path in files_path:
        os.remove(TEMP_FILE_FOLDER_PATH+file_path)


def text_cleaner(text):
    text = text.lower()  # приведение в lowercase,
    text = re.sub(r'https?://[\S]+', ' ', text)  # замена интернет ссылок
    text = re.sub(r'[\w\./]+\.[a-z]+', ' ', text)
    text = re.sub(r'\d+:\d+(:\d+)?', ' ', text)
    text = re.sub(r'#\w+', ' ', text)  # замена хештегов
    text = re.sub(r'<[^>]*>', ' ', text)  # удаление html тагов
    text = re.sub(r'[\W]+', ' ', text)  # удаление лишних символов
    text = re.sub(r'\b\w\b', ' ', text)  # удаление отдельно стоящих букв
    text = re.sub(r'\b\d+\b', ' ', text)  # замена цифр

    return text


def get_files_of_a_thousand_words(file_path):
    clear_tmp()
    file = open(INPUT_PATH+file_path, 'r')
    text = file.read()
    text = text_cleaner(text)
    words = text.split(' ')
    tmp_text = ''
    for word in words:
        tmp_text += word + ' '
        if len(tmp_text.split(' ')) % NUMBER_OF_WORDS_IN_TMP_FILE == 0:
            tmp_file = open(TEMP_FILE_FOLDER_PATH+str(random.randint(0,100000))+'.txt', 'w')
            tmp_file.write(tmp_text)
            tmp_file.close()
            tmp_text = ''
    tmp_file = open(TEMP_FILE_FOLDER_PATH + str(random.randint(0, 100000)) + '.txt', 'w')
    tmp_file.write(tmp_text)
    tmp_file.close()
    return os.listdir(TEMP_FILE_FOLDER_PATH)


def copy_to_the_appropriate_directory(file_path, label):
    shutil.copy(INPUT_PATH+file_path, OUTPUT_PATH+str(label)+'/')


def clear_output():
    files_path = os.listdir(OUTPUT_PATH+'0/')
    for file_path in files_path:
        os.remove(OUTPUT_PATH+'0/' + file_path)

    files_path = os.listdir(OUTPUT_PATH+'1/')
    for file_path in files_path:
        os.remove(OUTPUT_PATH+'1/' + file_path)

    files_path = os.listdir(OUTPUT_PATH+'2/')
    for file_path in files_path:
        os.remove(OUTPUT_PATH+'2/' + file_path)


def main():
    clear_output()
    model = load_model()
    files_path = load_input_files_list()
    for file_path in files_path:
        tmp_files_list = get_files_of_a_thousand_words(file_path)
        label = model.predict(tmp_files_list)
        copy_to_the_appropriate_directory(file_path, label)
    clear_tmp()
    print('Success!')


if __name__ == '__main__':
    main()