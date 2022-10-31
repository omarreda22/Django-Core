class CustomMixins(object):
    title = "It's Default Title"
    # add = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = self.title
        context['add'] = self.add
        return context
