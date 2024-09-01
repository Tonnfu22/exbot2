from aiogram.utils.i18n import I18n

i18n = I18n(path='locales')

def get_translations(lang):
    return i18n.get_translations(lang)