from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_ARRAY, TYPE_STRING

NO_CONTENT = 'NO_CONTENT'


class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    """Adds default response handling for each endpoint
    (i. e. `400`, `500` etc)
    """

    def get_responses(self):
        responses = super().get_responses()

        if '400' not in responses:
            responses['400'] = Schema(
                title='Validation error',
                description='Data validation error',
                type=TYPE_OBJECT,
                properties={
                    'nonFieldError': Schema('Object specific error',
                                            type=TYPE_ARRAY,
                                            items=Schema('Bad data provided', type=TYPE_STRING)),
                    '[fieldName]': Schema('Field specific error',
                                          description='Validation errors for some field with `fieldName`',
                                          type=TYPE_ARRAY,
                                          items=Schema('Bad field data provided', type=TYPE_STRING))
                }
            )

        if '500' not in responses:
            responses['500'] = Schema(
                title='Server error',
                description='That must be rare. Ideally, not to happen at all',
                type=TYPE_STRING,
            )

        if self.method == 'GET':
            if '404' not in responses:
                responses['404'] = Schema(
                    title='Not found error',
                    description='Object with the provided parameters not found',
                    type=TYPE_OBJECT,
                    properties={'detail': Schema("Not found (or what exactly wasn't found)", type=TYPE_STRING)}
                )

        return responses
