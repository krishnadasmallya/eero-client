from .client import Client
from .exception import ClientException
import re
from datetime import datetime, timedelta

class Eero(object):
    def __init__(self, session):
        # type(SessionStorage) -> ()
        self.session = session
        self.client = Client()

    @property
    def _cookie_dict(self):
        if self.needs_login():
            return dict()
        else:
            return dict(s=self.session.cookie)

    def needs_login(self):
        return self.session.cookie is None

    def login(self, identifier):
        # type(string) -> string
        json = dict(login=identifier)
        data = self.client.post("login", json=json)
        return data["user_token"]

    def login_verify(self, verification_code, user_token):
        json = dict(code=verification_code)
        response = self.client.post(
            "login/verify", json=json, cookies=dict(s=user_token)
        )
        self.session.cookie = user_token
        return response

    def refreshed(self, func):
        try:
            return func()
        except ClientException as exception:
            if (
                exception.status == 401
                and exception.error_message == "error.session.refresh"
            ):
                self.login_refresh()
                return func()
            else:
                raise

    def login_refresh(self):
        response = self.client.post("login/refresh", cookies=self._cookie_dict)
        self.session.cookie = response["user_token"]

    def account(self):
        return self.refreshed(
            lambda: self.client.get("account", cookies=self._cookie_dict)
        )

    def id_from_url(self, id_or_url):
        match = re.search("^[0-9]+$", id_or_url)
        if match:
            return match.group(0)
        match = re.search(r"\/([0-9]+)$", id_or_url)
        if match:
            return match.group(1)

    def networks(self, network_id):
        return self.refreshed(
            lambda: self.client.get(
                "networks/{}".format(self.id_from_url(network_id)),
                cookies=self._cookie_dict,
            )
        )

    def devices(self, network_id):
        return self.refreshed(
            lambda: self.client.get(
                "networks/{}/devices".format(self.id_from_url(network_id)),
                cookies=self._cookie_dict,
            )
        )

    def eeros(self, network_id):
        return self.refreshed(
            lambda: self.client.get(
                "networks/{}/eeros".format(self.id_from_url(network_id)),
                cookies=self._cookie_dict,
            )
        )

    def device(self, network_id, device_id):
        return self.refreshed(
            lambda: self.client.get(
                "networks/{}/devices/{}".format(network_id, device_id),
                cookies=self._cookie_dict,
            )
        )

    def reboot(self, device_id):
        return self.refreshed(
            lambda: self.client.post(
                "eeros/{}/reboot".format(self.id_from_url(device_id)),
                cookies=self._cookie_dict,
            )
        )

    def data_usage_hour(self, network_id, start, end):
        return self.refreshed(
            lambda: self.client.get(
                "networks/{}/data_usage?start={}&end={}&cadence=hourly".format(network_id, start, end),
                cookies=self._cookie_dict,
            )
        )

    def data_usage_last_hour(self, network_id):
        current_time = datetime.utcnow() - timedelta(hours=1)
        end = self.ceil_dt_min(current_time, timedelta(hours=1))
        start = end - timedelta(hours=1)
        return self.data_usage_hour(network_id, start.isoformat(timespec='milliseconds'), end.isoformat(timespec='milliseconds'))

    def data_usage_5_min_breakdown(self, network_id, start, end):
        return self.refreshed(
            lambda: self.client.get(
                "networks/{}/data_usage/breakdown?start={}&end={}".format(network_id, start, end),
                cookies=self._cookie_dict,
            )
        )

    def data_usage_last_5_min_breakdown(self, network_id):
        # FIXME: consider latency in the data. Look from 10 mins back
        latency_adjustment=5
        current_time = datetime.utcnow() - timedelta(minutes=latency_adjustment+10)
        end = self.ceil_dt_min(current_time, timedelta(minutes=latency_adjustment))
        start = end - timedelta(minutes=latency_adjustment)
        return self.data_usage_5_min_breakdown(network_id, start.isoformat(timespec='milliseconds'), end.isoformat(timespec='milliseconds'))

    def ceil_dt_min(self, dt, delta):
        return dt + (datetime.min - dt) % delta

    def ceil_dt_hour(self, dt, delta):
        return dt + (datetime.hour - dt) % delta

    def start_speed_test(self, network_id):
        return self.refreshed(
            lambda: self.client.post(
                "networks/{}/speedtest".format(network_id),
                cookies=self._cookie_dict,
            )
        )

    def get_speed_test(self, network_id):
        return self.refreshed(
            lambda: self.client.get(
                "networks/{}/speedtest".format(network_id),
                cookies=self._cookie_dict,
            )
        )