import sublime
import sublime_plugin
import re
import random
import webcolors

def darken(hex, amount):
    hex = hex.replace('#','')
    r = int(hex[0:2], 16)
    g = int(hex[2:4], 16)
    b = int(hex[4:6], 16)

def color_variant(hex_color, brightness_offset=1):
    if len(hex_color) != 7:
        raise Exception("Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
    rgb_hex = [hex_color[x:x+2] for x in [1, 3, 5]]
    new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
    new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int]
    return "#" + "".join([hex(int(i))[2:] for i in new_rgb_int])


def lighten(hex, amount):
    """ Lighten an RGB color by an amount (between 0 and 1),

    e.g. lighten('#F56565', .5) = #C1FFFF
    """
    hex = hex.replace('#','')
    red = min(255, int(hex[0:2], 16) + 255 * amount)
    green = min(255, int(hex[2:4], 16) + 255 * amount)
    blue = min(255, int(hex[4:6], 16) + 255 * amount)
    return "#%X%X%X" % (int(red), int(green), int(blue))

class SublimeTailwindShadesCommand(sublime_plugin.WindowCommand):
    def run(self):
        print('SublimeTailwindShadesCommand called')
        window = self.window
        view = window.active_view()
        sel = view.sel()
        region1 = sel[0]
        selectedText = view.substr(region1)
        base = '''{
'''.format('webcolors')
        
        generatedCode += base
        for lightenFactor in [10,20,30,40,50,60,70,80,90]:
            generatedCode += "\t{}: {}\n".format((100 - lightenFactor) * 10, color_variant(selectedText, lightenFactor))
        generatedCode += '}'

        view.run_command( 'sublime_tailwind_shades_helper', { 'generatedCode' : generatedCode } )


class SublimeTailwindShadesHelperCommand(sublime_plugin.TextCommand):
    def run(self, edit, generatedCode = None):
        self.view.insert(edit, 0, generatedCode)
