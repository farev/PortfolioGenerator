from PIL import Image

def main(img_path, out_path, func):
    img = Image.open(img_path)
    img = img.convert("RGBA")
    new_data = func(img.getdata())
    img.putdata(new_data)
    img.save(out_path, "PNG")

def make_white_transparent(data):
    new_data = []
    for item in data:
        avg = (item[0] + item[1] + item[2]) / 3 - 100
        avg = max(avg, 0)
        transparency = (255 - avg)
        new_data.append((item[0], item[1], item[2], int(transparency)))
    return new_data

def make_black_transparent(data):
    new_data = []
    for item in data:
        avg = (item[0] + item[1] + item[2]) / 3 + 100
        avg = min(avg, 255)
        transparency = avg
        new_data.append((item[0], item[1], item[2], int(transparency)))
    return new_data

if __name__ == '__main__':
    main("./logo/logo_black.jpeg", "./logo/logo_black_transparent.png", make_white_transparent)
    main("./logo/logo_white.jpeg", "./logo/logo_white_transparent.png", make_black_transparent)