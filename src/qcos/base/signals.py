from django.dispatch.dispatcher import Signal
from django.conf import settings
from django.dispatch.dispatcher import NO_RECEIVERS
from django.apps import apps
from qcos.base.models import Camp
from typing import Any, Callable, List, Tuple

app_cache = dict()


app_cache = {}


def _populate_app_cache():
    global app_cache
    apps.check_apps_ready()
    for ac in apps.app_configs.values():
        app_cache[ac.name] = ac


class CampPluginSignal(Signal):

    def _is_active(self, sender, receiver):
        if sender is None:
            # Send to all events!
            return True

        # Find the Django application this belongs to
        searchpath = receiver.__module__
        core_module = any([searchpath.startswith(cm) for cm in settings.CORE_MODULES])
        app = None
        if not core_module:
            while True:
                app = app_cache.get(searchpath)
                if "." not in searchpath or app:
                    break
                searchpath, _ = searchpath.rsplit(".", 1)

        # Only fire receivers from active plugins and core modules
        excluded = settings.PRETIX_PLUGINS_EXCLUDE
        if core_module or (sender and app and app.name in sender.get_plugins() and app.name not in excluded):
            if not hasattr(app, 'compatibility_errors') or not app.compatibility_errors:
                return True
        return False

    def send(self, sender: Camp, **named) -> List[Tuple[Callable, Any]]:
        """
        Send signal from sender to all connected receivers that belong to
        plugins enabled for the given Event.
        sender is required to be an instance of ``pretix.base.models.Event``.
        """
        if sender and not isinstance(sender, Camp):
            raise ValueError("Sender needs to be an event.")

        responses = []
        if not self.receivers or self.sender_receivers_cache.get(sender) is NO_RECEIVERS:
            return responses

        if not app_cache:
            _populate_app_cache()

        for receiver in self._sorted_receivers(sender):
            if self._is_active(sender, receiver):
                response = receiver(signal=self, sender=sender, **named)
                responses.append((receiver, response))
        return responses

    def send_chained(self, sender: Camp, chain_kwarg_name, **named) -> List[Tuple[Callable, Any]]:
        """
        Send signal from sender to all connected receivers. The return value of the first receiver
        will be used as the keyword argument specified by ``chain_kwarg_name`` in the input to the
        second receiver and so on. The return value of the last receiver is returned by this method.
        sender is required to be an instance of ``pretix.base.models.Event``.
        """
        if sender and not isinstance(sender, Camp):
            raise ValueError("Sender needs to be an event.")

        response = named.get(chain_kwarg_name)
        if not self.receivers or self.sender_receivers_cache.get(sender) is NO_RECEIVERS:
            return response

        if not app_cache:
            _populate_app_cache()

        for receiver in self._sorted_receivers(sender):
            if self._is_active(sender, receiver):
                named[chain_kwarg_name] = response
                response = receiver(signal=self, sender=sender, **named)
        return response

    def send_robust(self, sender: Camp, **named) -> List[Tuple[Callable, Any]]:
        """
        Send signal from sender to all connected receivers. If a receiver raises an exception
        instead of returning a value, the exception is included as the result instead of
        stopping the response chain at the offending receiver.
        sender is required to be an instance of ``pretix.base.models.Event``.
        """
        if sender and not isinstance(sender, Camp):
            raise ValueError("Sender needs to be an event.")

        responses = []
        if (
            not self.receivers
            or self.sender_receivers_cache.get(sender) is NO_RECEIVERS
        ):
            return []

        if not app_cache:
            _populate_app_cache()

        for receiver in self._sorted_receivers(sender):
            if self._is_active(sender, receiver):
                try:
                    response = receiver(signal=self, sender=sender, **named)
                except Exception as err:
                    responses.append((receiver, err))
                else:
                    responses.append((receiver, response))
        return responses

    def _sorted_receivers(self, sender):
        orig_list = self._live_receivers(sender)
        sorted_list = sorted(
            orig_list,
            key=lambda receiver: (
                0 if any(receiver.__module__.startswith(m) for m in settings.CORE_MODULES) else 1,
                receiver.__module__,
                receiver.__name__,
            )
        )
        return sorted_list

