from drf_spectacular.utils import PolymorphicProxySerializer
from drf_standardized_errors.openapi_serializers import ClientErrorEnum, ParseErrorCodeEnum,   ParseErrorResponseSerializer, ValidationErrorEnum
from drf_standardized_errors.openapi import AutoSchema
from drf_standardized_errors.settings import package_settings
from inflection import camelize
from rest_framework import serializers
from typing import Type, Dict, Any, Optional, Set, List

class CustomAutoSchema(AutoSchema):
    def _get_http400_serializer(self):
        operation_id = self.get_operation_id()
        component_name = f"{camelize(operation_id)}ErrorResponse400"

        http400_serializers = {}
        if self._should_add_validation_error_response():

            fields_with_error_codes = self._determine_fields_with_error_codes()
            error_codes_by_field = self._get_validation_error_codes_by_field(
                fields_with_error_codes
            )

            serializer = get_validation_error_serializer(operation_id, error_codes_by_field)
            http400_serializers[ValidationErrorEnum.VALIDATION_ERROR.value] = serializer  # type: ignore[attr-defined]
        if self._should_add_parse_error_response():
            serializer = ParseErrorResponseSerializer
            http400_serializers[ParseErrorCodeEnum.PARSE_ERROR.value] = serializer  # type: ignore[attr-defined]



        return PolymorphicProxySerializer(
            component_name=component_name,
            serializers=http400_serializers,
            resource_type_field_name="type",
        )


def get_validation_error_serializer(
    operation_id: str, error_codes_by_field: Dict[str, Set[str]]
)-> Type[serializers.Serializer]:
    validation_error_component_name = f"{camelize(operation_id)}ValidationError"
    errors_component_name = f"{camelize(operation_id)}Error"
    fields: List[str] = [ field_name for field_name,_ in error_codes_by_field.items()]

    component_name = f"{camelize(operation_id)}ValidationItemError"

    attr_kwargs: Dict[str, Any] = {"choices": [(attr, attr) for attr in fields]}

    class ValidationItemError(serializers.Serializer):
        attr = serializers.ChoiceField(**attr_kwargs)
        code = serializers.CharField()
        detail = serializers.CharField()

        class Meta:
            ref_name = component_name


    class ValidationErrorSerializer(serializers.Serializer):
        type = serializers.ChoiceField(choices=ValidationErrorEnum.choices)
        errors = ValidationItemError(many=True)

        class Meta:
            ref_name = validation_error_component_name

    return ValidationErrorSerializer


class Error401Serializer(serializers.Serializer):
    code = serializers.CharField()
    detail = serializers.CharField()
    attr = serializers.CharField(allow_null=True)


class ErrorResponse401Serializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=ClientErrorEnum.choices)
    errors = Error401Serializer(many=True)
