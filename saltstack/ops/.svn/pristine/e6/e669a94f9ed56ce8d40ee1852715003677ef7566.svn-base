from rest_framework import mixins, generics


class ListCreateUpdateDestroyAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                                     mixins.DestroyModelMixin, generics.GenericAPIView):

    # list
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # create
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # update
    def put(self, request, *args, **kwargs):
        id = int(request.data['id'])
        kwargs['id'] = id
        kwargs['pk'] = id
        self.kwargs = kwargs
        return self.update(request, *args, **kwargs)

    # delete
    def delete(self, request, *args, **kwargs):
        id = int(request.data['id'])
        kwargs['id'] = id
        kwargs['pk'] = id
        self.kwargs = kwargs
        return self.destroy(request, *args, **kwargs)
