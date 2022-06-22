import pyaudio

running = 1

# установить размер блока в 1024 сэмпла
chunk = 1024
# образец формата
FORMAT = pyaudio.paInt16
# моно, если хотите стере измените на 2
channels = 1
# 44100 сэмплов в секунду
sample_rate = 44100
# initialize PyAudio object
p = pyaudio.PyAudio()
# открыть объект потока как ввод и вывод
stream = p.open(format=FORMAT,
                channels=channels,
                rate=sample_rate,
                input=True,
                output=True,
                frames_per_buffer=chunk)


def main():
    while running == 1:
        data = stream.read(chunk)

        # если вы хотите слышать свой голос во время записи
        stream.write(data)

    # # остановить и закрыть поток
    stream.stop_stream()
    stream.close()
    # # завершить работу объекта pyaudio
    p.terminate()


if __name__ == "__main__":
    main()
