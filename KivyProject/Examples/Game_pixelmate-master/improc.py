import zipfile

from kivy.graphics.fbo import Fbo
from kivy.graphics.texture import Texture
from kivy.graphics.opengl import glReadPixels, GL_RGBA, GL_RGB, GL_UNSIGNED_BYTE
from kivy.graphics.opengl import glBlendFunc, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from kivy.graphics import Color, Rectangle
from PIL import Image as PILImage

from dialog import PopupMessage


def texture_get_data(texture):
    size = texture.size
    fbo = Fbo(size=texture.size, texture=texture)
    fbo.draw()
    fbo.bind()
    data = glReadPixels(0, 0, size[0], size[1], GL_RGBA, GL_UNSIGNED_BYTE)
    fbo.release()
    return data


def texture_to_pil_image(texture):
    size = texture.size
    fbo = Fbo(size=texture.size, texture=texture)
    fbo.draw()
    fbo.bind()
    data = glReadPixels(0, 0, size[0], size[1], GL_RGBA, GL_UNSIGNED_BYTE)
    fbo.release()
    im = PILImage.fromstring('RGBA', size, data)
    return im


def texture_flip(texture):
    pil_image = texture_to_pil_image(texture)
    im = pil_image.transpose(PILImage.FLIP_TOP_BOTTOM)
    string = im.tostring()
    texture.blit_buffer(string, colorfmt='rgba', bufferfmt='ubyte')
    return texture


def load_texture(path):
    image = PILImage.open(path)
    string = image.tostring()
    texture = Texture.create(size=image.size, colorfmt='rgba')
    texture.mag_filter = 'nearest'
    texture.min_filter = 'nearest'
    texture.blit_buffer(string, colorfmt='rgba', bufferfmt='ubyte')
    return texture


def texture_save(texture, filename, format=None):
    size = texture.size
    fbo = Fbo(size=texture.size, texture=texture)
    fbo.draw()
    fbo.bind()
    if format == 'BMP':
        data = glReadPixels(0, 0, size[0], size[1], GL_RGB, GL_UNSIGNED_BYTE)
    else:
        data = glReadPixels(0, 0, size[0], size[1], GL_RGBA, GL_UNSIGNED_BYTE)
    fbo.release()
    if format == 'BMP':
        im = PILImage.fromstring('RGB', size, data)
    else:
        im = PILImage.fromstring('RGBA', size, data)
    im = im.transpose(PILImage.FLIP_TOP_BOTTOM)
    im.save(filename)


def texture_add_to_zip(texture, zip_object, entry_name):
    size = texture.size
    fbo = Fbo(size=texture.size, texture=texture)
    fbo.draw()
    fbo.bind()
    if format == 'BMP':
        data = glReadPixels(0, 0, size[0], size[1], GL_RGB, GL_UNSIGNED_BYTE)
    else:
        data = glReadPixels(0, 0, size[0], size[1], GL_RGBA, GL_UNSIGNED_BYTE)
    fbo.release()
    zip_object.writestr(entry_name, data)


def textures_list_save_to_zip(tex_list, filename):
    zip_object = zipfile.ZipFile(filename, mode='w', compression=zipfile.ZIP_DEFLATED)
    index = 0
    for texture in tex_list:
        texture_add_to_zip(texture, zip_object, str(index) + '.buffer')
        index += 1
    zip_object.comment = str(tex_list[0].size[0]) + ',' + str(tex_list[0].size[1])
    zip_object.close()


def textures_list_from_zip(filename):
    if zipfile.is_zipfile(filename):
        zip_object = zipfile.ZipFile(filename, 'r')
        size = [int(x) for x in zip_object.comment.split(',')]
        textures_list = []
        for info in zip_object.infolist():
            buffer = zip_object.read(info)

            tex = Texture.create(size=size, colorfmt='rgba', bufferfmt='ubyte')
            tex.mag_filter = 'nearest'
            tex.min_filter = 'nearest'
            tex.blit_buffer(buffer, colorfmt='rgba', bufferfmt='ubyte')
            textures_list.append(tex)
        return textures_list
    else:
        PopupMessage(title='Caution', text='Unable to open file')


def merged_texture_from_zip(filename):
    textures_list = textures_list_from_zip(filename)
    fbo = Fbo(size=textures_list[0].size)
    fbo.bind()
    with fbo:
        for texture in textures_list:
            Rectangle(texture=texture)
    fbo.release()
    fbo.draw()
    return fbo.texture


def widget_save_canvas(widget, filename, format):
    parent = widget.parent
    if parent:
        parent.remove_widget(widget)
    size = (int(widget.size[0]), int(widget.size[1]))
    texture = Texture.create(size=widget.size, colorfmt='rgba')
    fbo = Fbo(size=widget.size, texture=texture)
    fbo.add(widget.canvas)
    fbo.draw()
    fbo.bind()
    data = glReadPixels(0, 0, size[0], size[1], GL_RGBA, GL_UNSIGNED_BYTE)
    fbo.release()
    im = PILImage.fromstring('RGBA', size, data)
    im = im.transpose(PILImage.FLIP_TOP_BOTTOM)
    im.save(filename, format)
    if parent:
        parent.add_widget(widget)
    return True


def texture_copy(texture, smooth=False):
    buf = texture.pixels
    tex = Texture.create(size=texture.size, colorfmt='rgba', bufferfmt='ubyte')
    if not smooth:
        tex.mag_filter = 'nearest'
        tex.min_filter = 'nearest'
    tex.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
    return tex


def texture_copy_region(texture, (x, y, w, h)):
    text_reg = texture.get_region(x, y, w, h)
    buf = text_reg.pixels
    tex = Texture.create(size=(w, h), colorfmt='rgba', bufferfmt='ubyte')
    tex.mag_filter = 'nearest'
    tex.min_filter = 'nearest'
    tex.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
    return tex


def texture_merge(texture1, texture2):
    fbo = Fbo(size=texture2.size, texture=texture2)
    fbo.add(Rectangle(pos=(0, 0), texture=texture1, size=texture1.size))
    fbo.draw()
    return fbo.texture


def texture_replace_data(target_tex, source_tex):
    target_tex.blit_buffer(source_tex.pixels, colorfmt='rgba', bufferfmt='ubyte')


def texture_replace_color(tex, pos, color, size=(1, 1)):
    sz = size[0] * size[1] * 4
    buf = [color for x in xrange(sz)]
    buf = ''.join(map(chr, buf))
    tex.blit_buffer(buf, pos=pos, size=size, colorfmt='rgba', bufferfmt='ubyte')
    return tex


def new_color(texture, color, x, y, fbo):
    with fbo:
        tex_region = texture.get_region(x, y, 4, 4)
        fbo.add(color)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        Rectangle(size=(4, 4), pos=(x, y), texture=tex_region)


def get_pixels(fbo, (x, y)):
    fbo.bind()
    data = glReadPixels(x, y, 1, 1, GL_RGBA, GL_UNSIGNED_BYTE)
    fbo.release()
    c = [ord(a) for a in data]
    return c


def binded_fbo_get_pixels(fbo, (x, y)):
    data = glReadPixels(x, y, 1, 1, GL_RGBA, GL_UNSIGNED_BYTE)
    c = [ord(a) for a in data]
    return c


_fill_queue = []
_fill_width = 0
_fill_height = 0


def _fill_check(fbo, (x, yu, yd), c, flabel):
    global _fill_queue, _fill_height
    iu = yu
    fqueue = _fill_queue
    fheight = _fill_height
    if iu >= 0 and flabel[x][iu] == 0 and binded_fbo_get_pixels(fbo, (x, iu)) == c:
        f = 0
    else:
        f = 1
    while iu >= 0 and flabel[x][iu] == 0 and binded_fbo_get_pixels(fbo, (x, iu)) == c:
        iu -= 1
    iu += 1
    i = iu
    id = yu
    for id in xrange(yu, yd):
        if flabel[x][id] == 0 and binded_fbo_get_pixels(fbo, (x, id)) == c:
            if f:
                f = 0
                i = id
        else:
            if f == 0:
                fqueue += [(x, i, id)]
                f = 1
    if f == 0:
        while id < fheight and flabel[x][id] == 0 and binded_fbo_get_pixels(fbo, (x, id)) == c:
            id += 1
        fqueue += [(x, i, id)]
    _fill_queue = fqueue
    flabel[x][iu:id] = (id - iu) * [1]
    return flabel


def fillimage(fbo, (x, y), color):
    global _fill_queue, _fill_height, _fill_width
    _fill_width, _fill_height = fbo.texture.size
    if not (0 <= x < _fill_width and 0 <= y < _fill_height):
        return 0
    if type(color) == type(1):
        cr = color / 65536
        cg = (color % 65536) / 256
        cb = color % 256
        color = (cr, cg, cb)
    c = get_pixels(fbo, (x, y))
    if color == c:
        return 0
    _fill_queue = []
    flabel = []
    for i in xrange(_fill_width):
        s = []
        for j in xrange(_fill_height):
            s += [0]
        flabel += [s]
    fbo.bind()
    flabel = _fill_check(fbo, (x, y, y + 1), c, flabel)
    fbo.add(Color(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0))
    while _fill_queue:
        x, yu, yd = _fill_queue[0]
        _fill_queue = _fill_queue[1:]
        fbo.add(Rectangle(pos=(x, yd), size=(1, yu - yd)))
        flabel[x][yu:yd] = (yd - yu) * [1]
        if x > 0: flabel = _fill_check(fbo, (x - 1, yu, yd), c, flabel)
        if x < _fill_width - 1: flabel = _fill_check(fbo, (x + 1, yu, yd), c, flabel)
    fbo.release()
    fbo.draw()


