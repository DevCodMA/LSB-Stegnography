from random import seed, sample

def XOR(pix_data, pswd, length, msg_data):
    seed(pswd)
    t_str = ""
    index = sample(range(len(pix_data)), length)

    for i, j in zip(range(length), index):
        t_str += str(int(msg_data[i]) ^ int(pix_data[j]))

    return t_str


# Convert data to 8-bit binary form
def data2Bin(data):
    if type(data) == str:
        return ''.join((format(ord(i), '08b') for i in data))
    elif type(data) == tuple:
        return tuple(format(i, '08b') for i in data)


def encode(img, pswd, msg):
    print("Encoding process started....")
    print(f"Image pixel count: {len(img)}, Message length: {len(msg)}")
    try:
        if len(msg) > len(img)-2:
            raise ValueError("Need a large image!")

        msg = data2Bin(chr(247)+msg+chr(248))

        # Setting password
        seed(pswd)

        # Splitting the data into an 8-bit form
        msg_set = [msg[i: i + 8] for i in range(0, len(msg), 8)]



        # Randomly taken all the pixel index values based on the given password
        try:
            pixel_index = sample(range(len(img)), len(img))
            # Adding message to given image
            img = list(img)
            for i, val in enumerate(msg_set):
                index = pixel_index[i]
                im_data = list(data2Bin(img[index]))
                t_data = []

                red, green, blue = im_data[0][:5], im_data[1][:5], im_data[2][:6]
                msg_grp1, msg_grp2, msg_grp3 = val[0:3], val[3:6], val[6:8]

                # Adding 3-bit to red
                t_data.append(int(red + XOR(red, pswd, 3, msg_grp1), 2))
                # t_data.append(int(im_data[0][:5] + val[0:3], 2))
                # t_data.append(int(red + msg_grp1, 2))

                # Adding 3-bit to green
                t_data.append(int(green + XOR(green, pswd, 3, msg_grp2), 2))
                # t_data.append(int(im_data[1][:5] + val[3:6], 2))
                # t_data.append(int(green + msg_grp2, 2))

                # Adding 2-bit to blue
                t_data.append(int(blue + XOR(blue, pswd, 2, msg_grp3), 2))
                # t_data.append(int(im_data[2][:6] + val[6:8], 2))
                # t_data.append(int(blue + msg_grp3, 2))


                img[index] = tuple(t_data)

            print("Encoding process finished!")
            return img

        # Checking the image is suitable for storing the message (message is in 8-bit form)
        except Exception as ex:
            print("Encoding process halted!")
            print(f"Error: {ex}")
            return f"{ex}"

    except Exception as ex:
        print(ex)

def  decode(img, pswd):
    extension = ""
    numset = []
    start =True
    seed(pswd)
    print("Decoding process started....")
    try:
        pixel_index = sample(range(len(img)), len(img))
        img = list(img)
        catstr = ''
        for val, i in zip(img, pixel_index):
            im_data = list(data2Bin(img[i]))

            red, green, blue = im_data[0][:5], im_data[1][:5], im_data[2][:6]
            msg_grp1, msg_grp2, msg_grp3 = im_data[0][5:], im_data[1][5:], im_data[2][6:]
            # red
            # t_data = im_data[0][5:]
            t_data = XOR(red, pswd, 3, msg_grp1)
            # t_data = msg_grp1

            # green
            # t_data += im_data[1][5:]
            t_data += XOR(green, pswd, 3, msg_grp2)
            # t_data += msg_grp2

            # blue
            # t_data += im_data[2][6:]
            t_data += XOR(blue, pswd, 2, msg_grp3)

            # t_data += msg_grp3
            t_str = chr(int(t_data, 2))

            if t_str != chr(247) and start:
                return chr(247), chr(247)

            if t_str == chr(248):
                break

            start = False
            catstr += t_str

            if t_str == chr(254):
                extension = catstr[1:-1]
                catstr = ""

        print("Decoding process finished....")
        return extension, catstr

    except Exception as ex:
        print("Decoding process halted!")
        print(f"Error: {ex}")
        return chr(247), chr(247)
