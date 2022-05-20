import json

from utils.SaveStream import SaveStream


if __name__ == '__main__':
    print("Start Data Generation")
    saveStream = SaveStream()

    data = saveStream.get_recent_stream(count=50)

    try:
        with open('data.json', 'w') as f:
            f.write(json.dumps(data, indent=4))
            print("Data Generation Complete")
    except BaseException as e:
        print("Error : %s" % str(e))
