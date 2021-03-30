from graphql import GraphQLError


class Validation:

    def check_is_date_empty(value, field):
        if value is None or value == '':
            raise GraphQLError("{0} field can't be empty".format(field.title()))

    def check_is_empty(value, field):
        if value is None or value == '' or value.isspace():
            raise GraphQLError("{0} field can't be empty".format(field.title()))