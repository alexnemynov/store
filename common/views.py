class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):  # переопределяем метод get_context_data, чтобы добавить к атрибутам title
        ''' get_context_data находится в классе ContexMixin, который в свою очередь находится в классе TemplateView '''
        context = super(TitleMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context