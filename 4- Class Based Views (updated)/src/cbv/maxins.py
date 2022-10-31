# the default data for CBV
class ProductMixins(object):
    title = None
    omar = 'ahmed'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = self.get_title()
        context['omar'] = self.omar
        return context

    def get_title(self):
        return self.title
