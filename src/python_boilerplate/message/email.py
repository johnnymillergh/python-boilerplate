import smtplib
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any

from loguru import logger

from python_boilerplate.common.debounce_throttle import debounce
from python_boilerplate.configuration.application_configuration import application_conf
from python_boilerplate.template.html_template import render_template

_email_muted: bool = application_conf.get_bool("email.muted")
_muted_message = "Email module is muted!"
_host: str = application_conf.get_string("email.host")
_port: int = application_conf.get_int("email.port")
_username: str = application_conf.get_string("email.username")
_password: str = application_conf.get_string("email.password")
_sender: str = f"{_username}{application_conf.get_string('email.mail_address_suffix')}"
_receivers: list[str] = application_conf.get_list("email.receivers")

_smtp: smtplib.SMTP


def init_smtp() -> None:
    """Initialize the email module and log in to the SMTP server (no-op when muted)."""
    global _smtp
    if _email_muted or _email_muted is None:
        logger.warning(_muted_message)
        return
    _smtp = smtplib.SMTP(_host, _port)
    _smtp.connect(_host, 25)
    _smtp.login(_sender, _password)
    logger.warning(f"Initialized email module and logged in to the email server: {_host}")


def build_message(
    subject: str,
    receiver: str,
    template_name: str,
    render_dict: dict[str, Any],
    picture_path: str,
) -> MIMEMultipart:
    """
    Builds a message with the given subject, receiver, template name and render dict.

    :param subject: The subject of the message.
    :param receiver: The receiver of the message.
    :param template_name: The name of the template to render.
    :param render_dict: The render dict for the template.
    :param picture_path: The path to the picture to attach.
    """
    content: MIMEText = MIMEText(
        render_template(template_name, render_dict),
        "html",
        "utf-8",
    )
    message: MIMEMultipart = MIMEMultipart("related")
    message["Subject"] = Header(subject, "utf-8").encode()
    message["From"] = Header(_sender, "utf-8").encode()
    message["To"] = Header(receiver, "utf-8").encode()
    message["Cc"] = Header(_sender, "utf-8").encode()
    message.attach(content)
    with Path(picture_path).open("rb") as file:
        img_data = file.read()
    img = MIMEImage(img_data)
    img.add_header("Content-ID", render_dict["content_id"])
    message.attach(img)
    return message


@debounce(10)
def send_email(subject: str, template_name: str, render_dict: dict[str, Any], picture_path: str) -> None:
    """
    Sends an email with the given subject, template name and render dict.

    :param subject: The subject of the message.
    :param template_name: The name of the template to render.
    :param render_dict: The render dict for the template.
    :param picture_path: The path to the picture to attach.
    """
    if _email_muted:
        logger.warning(_muted_message)
        return
    for receiver in _receivers:
        message: MIMEMultipart = build_message(subject, receiver, template_name, render_dict, picture_path)
        logger.info(f"Sending email. receiver: {receiver}")
        try:
            _smtp.sendmail(_sender, [receiver], message.as_string())
            logger.info(
                f"Sent email successfully. Receiver: {receiver}, subject: {subject}, template_name: {template_name}"
            )
        except smtplib.SMTPException:
            logger.exception("Exception occurred while sending email!")


def cleanup() -> None:
    """Closes the connection to the email server."""
    if _email_muted:
        logger.warning(_muted_message)
        return
    _smtp.quit()
    logger.warning(f"Logged out from the email server: {_host}")
