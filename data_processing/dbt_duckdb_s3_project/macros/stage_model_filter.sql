{% macro date_filter(column_name, start_date) %}
    {{ column_name }} >= '{{ start_date }}'::timestamp
    and {{ column_name }} < '{{ start_date }}'::timestamp + INTERVAL '1 month'
{% endmacro %}
