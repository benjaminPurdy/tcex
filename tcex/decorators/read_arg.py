# -*- coding: utf-8 -*-
"""ReadArg App Decorators."""
import wrapt


class ReadArg:
    """Read value of App arg resolving any playbook variables.

    This decorator will read the args from Redis, if it is a playbook variable, and pass the
    resolved value to the function.

    .. code-block:: python
        :linenos:
        :lineno-start: 1

        @ReadArg(arg='color', default='red')
        @ReadArg(arg='number')
        @ReadArg(
            arg='fruits',
            array=True,
            fail_on=[None, []],
            fail_enabled=True,
            fail_msg='Invalid input for fruits'
        )
        def my_method(self, color, number, fruits):
            print('color', color)
            print('number', number)
            print('fruit', fruit)

        # ** OR **

        @ReadArg(arg='color', default='red')
        @ReadArg(arg='number')
        @ReadArg(
            arg='fruits',
            array=True,
            fail_on=[None, []],
            fail_enabled=True,
            fail_msg='Invalid input for fruits'
        )
        def my_method(self, **kwargs):
            print('color', kwargs.get('color'))
            print('number', kwargs.get('number')
            print('fruit', kwargs.get('fruit')

    Args:
        arg (str): The arg name from the App which contains the input. This input can be
            a Binary, BinaryArray, KeyValue, KeyValueArray, String, StringArray, TCEntity, or
            TCEntityArray.
        array (bool, kwargs): Defaults to False. If True the arg value will always be
            returned as an array.
        default (str, kwargs): Defaults to None. Default value to pass to method if arg
            value is None. Only supported for String or StringArray.
        fail_enabled (boolean|str, kwargs): Accepts a boolean or string value.  If a boolean value
            is provided that value will control enabling/disabling this feature. A string
            value should reference an item in the args namespace which resolves to a boolean.
            The value of this boolean will control enabling/disabling this feature.
        fail_msg (str, kwargs): The message to log when raising RuntimeError.
        fail_on (list, kwargs): Defaults to None. Fail if data read from Redis is in list.
    """

    def __init__(self, arg, **kwargs):
        """Initialize Class properties"""
        self.arg = arg
        self.array = kwargs.get('array')
        self.default = kwargs.get('default')
        self.fail_enabled = kwargs.get('fail_enabled', True)
        self.fail_msg = kwargs.get('fail_msg', f'Invalid value provided for ({arg}).')
        self.fail_on = kwargs.get('fail_on', [])
        self.embedded = kwargs.get('embedded', True)

    @wrapt.decorator
    def __call__(self, wrapped, instance, args, kwargs):
        """Implement __call__ function for decorator.

        Args:
            fn (function): The decorated function.

        Returns:
            function: The custom decorator function.
        """

        def read(app, *args, **kwargs):
            """Retrieve/Read data from Redis.

            Args:
                app (class): The instance of the App class "self".
            """
            # self.enable (e.g., True or 'fail_on_false') enables/disables this feature
            enabled = self.fail_enabled
            if not isinstance(self.fail_enabled, bool):
                enabled = getattr(app.args, self.fail_enabled)
                if not isinstance(enabled, bool):  # pragma: no cover
                    raise RuntimeError(
                        'The fail_enabled value must be a boolean or resolved to bool.'
                    )
            app.tcex.log.debug(f'Fail enabled is {enabled} ({self.fail_enabled}).')

            # retrieve data from Redis and call decorated function
            arg_data = app.tcex.playbook.read(
                getattr(app.args, self.arg), self.array, embedded=self.embedded
            )
            arg_type = app.tcex.playbook.variable_type(getattr(app.args, self.arg))
            if self.default is not None and arg_data is None:
                arg_data = self.default
                app.tcex.log.debug(
                    f'replacing null value with provided default value "{self.default}".'
                )

            # check arg_data against fail_on_values
            if enabled and self.fail_on:
                if arg_data in self.fail_on:
                    app.tcex.log.error(f'Invalid value ({arg_data}) found for {self.arg}.')
                    app.exit_message = self.fail_msg  # for test cases
                    app.tcex.exit(1, self.fail_msg)

            # add results to kwargs
            kwargs[self.arg] = arg_data

            # Add logging for debug/troubleshooting
            if arg_type not in ['Binary', 'BinaryArray'] and app.tcex.log.getEffectiveLevel() <= 10:
                log_string = str(arg_data)
                if len(log_string) > 100:  # pragma: no cover
                    log_string = f'{log_string[:100]} ...'
                app.tcex.log.debug(f'input value: {log_string}')

            return wrapped(*args, **kwargs)

        return read(instance, *args, **kwargs)