# JTW mount config generator by Michel Moriniaux
from string import Template
import re
import textwrap
import os
import signal
import sys

# initialize the choices, default is index 0
choices = {
    'model': {
        'desc': 'What mount do you want to configure?',
        'items': [{
            'desc': 'GTR: Second generation Trident, usually configured with homing and PEC sensors, optional encoders',
            'item': 'GTR',
            'elig': 'A'}, {
            'desc': 'P75: First generation Trident, can be configured with encoders',
            'item': 'P75',
            'elig': 'A'}]},
    'board': {
        'desc': 'What type of controller do you have?',
        'items': [{
            'desc': 'Manticore',
            'item': 'MANTICORE',
            'elig': 'A'}, {
            'desc': 'Original Onstep Controller - USE AT YOUR OWN RISK THIS IS UNTESTED AND UNSUPPORTED',
            'item': 'MaxSTM3',
            'elig': 'A'}]},
    'options': {
        'desc': 'A descriptive string of enabled options',
        'items': [{'desc': '', 'item': ' - ', 'elig': 'A'}]},
    'wifi_mode': {
        'desc': 'Chose how you want to use wireless features',
        'items': [{
            'desc': 'The controller will behave as a Wifi access point, your computers can connect to it but it will not provide internet access. Features such as NTP will not be available',
            'item': 'WIFI_ACCESS_POINT',
            'elig': 'A'}, {
            'desc': 'The Controller will join your wifi network and will have access to the rest of your network including the internet',
            'item': 'WIFI_STATION',
            'elig': 'A'}, {
            'desc': 'The controller will deactivate the Wifi and will only be usable through Ethernet and USB for the Manticore and USB only on the legacy controllers. Note: if you chose this configuration on the Manticore you will have to delete the \'webserver\' plugin',
            'item': 'OFF',
            'elig': 'M'}, {
            'desc': 'Use this option to deactivate Wifi and enable Bluetooth. Use this option if you want to use a gamepad',
            'item': 'BLUETOOTH',
            'elig': 'M'}]},
    'ap_enabled': {
        'desc': 'Do you want to enable WIFI in access point mode?',
        'items': [{
            'desc': 'Wifi will be enabled in AP mode and disabled in client mode',
            'item': 'true',
            'elig': 'A'}, {
            'desc': 'Wifi will be disabled for AP mode',
            'item': 'false',
            'elig': 'A'}]},
    'ap_ssid': {
        'desc': 'Choose an SSID for the access point below or enter your own choice',
        'items': [{
            'desc': 'JTW Trident',
            'item': 'JTW Trident',
            'elig': 'A'}]},
    'ap_password': {
        'desc': 'Choose a password for the Wifi network or enter your own choice',
        'items': [{
            'desc': 'password',
            'item': 'password',
            'elig': 'A'}]},
    'ap_wifi_ip': {
        'desc': 'Enter the Access Point IP address, please enter the values as in the default choice',
        'items': [{
            'desc': '192.168.0.1',
            'item': '{192,168,0,1}',
            'elig': 'A'}]},
    'ap_wifi_mask': {
        'desc': 'Enter the Access Point Netmask, the default value if good for 99.99% of cases',
        'items': [{
            'desc': '255.255.255.0',
            'item': '{255,255,255,0}',
            'elig': 'A'}]},
    'sta_enabled': {
        'desc': 'Do you want to enable WIFI in client mode?',
        'items': [{
            'desc': 'Wifi will be enabled in AP mode and disabled in client mode',
            'item': 'false',
            'elig': 'A'}, {
            'desc': 'Wifi will be enabled for mode',
            'item': 'true',
            'elig': 'A'}]},
    'sta_ssid': {
        'desc': 'Enter the SSID of your Wifi network',
        'items': [{
            'desc': 'Home',
            'item': 'Home',
            'elig': 'A'}]},
    'sta_password': {
        'desc': 'Enter the password/key of your Wifi network',
        'items': [{
            'desc': 'password',
            'item': 'password',
            'elig': 'A'}]},
    'wifi_dhcp': {
        'desc': 'Do you want to enable DHCP for the wifi client?',
        'items': [{
            'desc': 'The controller will fetch an IP address from your router.',
            'item': 'true',
            'elig': 'A'}, {
            'desc': 'Set a static IP. The controller will not be assigned an IP adress from your router.',
            'item': 'false',
            'elig': 'A'}]},
    'sta_wifi_ip': {
        'desc': 'Enter the Controller\'s static IP address',
        'items': [{
            'desc': '192.168.1.55',
            'item': '{192,168,1,55}',
            'elig': 'A'}]},
    'sta_wifi_gw': {
        'desc': 'Enter your router\'s IP address',
        'items': [{
            'desc': '192.168.1.1',
            'item': '{192,168,1,1}',
            'elig': 'A'}]},
    'sta_wifi_mask': {
        'desc': 'Enter your wifi network\'s Netmask.',
        'items': [{
            'desc': '255.255.255.0',
            'item': '{255,255,255,0}',
            'elig': 'A'}]},
    'eth_dhcp': {
        'desc': 'Do you want to enable DHCP for the Ethernet port?',
        'items': [{
            'desc': 'The controller will fetch an IP address from your router.',
            'item': 'true',
            'elig': 'M'}, {
            'desc': 'Set a static IP. The controller will not be assigned an IP adress from your router',
            'item': 'false',
            'elig': 'M'}]},
    'eth_ip': {
        'desc': 'Enter the Controller\'s Ethernet port static IP address',
        'items': [{
            'desc': '192.168.1.56',
            'item': '{192,168,1,56}',
            'elig': 'M'}]},
    'eth_gw': {
        'desc': 'Enter your router\'s IP address',
        'items': [{
            'desc': '192.168.1.1',
            'item': '{192,168,1,1}',
            'elig': 'M'}]},
    'eth_mask': {
        'desc': 'Enter your wifi network\'s Netmask.',
        'items': [{
            'desc': '255.255.255.0',
            'item': '{255,255,255,0}',
            'elig': 'M'}]},
    'weather_mode': {
        'desc': 'Do you want to enable a Temperature Pressure Humidity probe? this probve is available from JTW and connects to the AUX port on the Manticore',
        'items': [{
            'desc': 'No, I do not have a BME680 TPH probe connected',
            'item': 'OFF',
            'elig': 'A'}, {
            'desc': 'Yes, I have an I2C TPH probe connected to the aux port of my manticore',
            'item': 'BME280_0x76',
            'elig': 'M'}]},
    'weather': {
        'desc': 'Do you want a display of the TPH data in the webserver?',
        'items': [{
            'desc': 'Yes',
            'item': 'ON',
            'elig': 'A'}, {
            'desc': 'No',
            'item': 'OFF',
            'elig': 'A'}]},
    'temp': {
        'desc': 'Do you want a display of the Controller\'s internal temperature in the webserver?',
        'items': [{
            'desc': 'Yes',
            'item': 'ON',
            'elig': 'A'}, {
            'desc': 'No',
            'item': 'OFF',
            'elig': 'A'}]},
    'monitor': {
        'desc': 'Do you want a display of the servo\' behavior in the webserver? ( this only applies to encoder equipped mounts on the Manticore)',
        'items': [{
            'desc': 'No',
            'item': 'OFF',
            'elig': 'A'}, {
            'desc': 'Yes',
            'item': 'ON',
            'elig': 'M'}]},
    'origin': {
        'desc': 'Do you want a display of the servo\' origin reset in the webserver? ( this only applies to encoder equipped mounts on the Manticore)',
        'items': [{
            'desc': 'No',
            'item': 'OFF',
            'elig': 'A'}, {
            'desc': 'Yes',
            'item': 'ON',
            'elig': 'M'}]},
    'calibration': {
        'desc': 'Do you want a display of the servo\' calibration controls in the webserver? ( this only applies to encoder equipped mounts on the Manticore)',
        'items': [{
            'desc': 'No',
            'item': 'OFF',
            'elig': 'A'}, {
            'desc': 'Yes',
            'item': 'ON',
            'elig': 'M'}]},
    'encoder': {
        'desc': 'What type of encoders does your mount have?',
        'items': [{
            'desc': 'My mount has no encoders',
            'item': 'OFF',
            'elig': 'A'}, {
            'desc': 'My mount has 24bit encoders (GTR, P75)',
            'item': 'JTW_24BIT',
            'elig': 'A'}, {
            'desc': 'My mount has 26bit encoders (GTR)',
            'item': 'JTW_26BIT',
            'elig': 'G'}, {
            'desc': 'My mount has 23bit encoders (P75)',
            'item': 'AS37_H39B_B',
            'elig': 'P'}]},
    'encoder_reverse': {
        'desc': 'Do you want to reverse the encoder directions? ( this only applies to encoder equipped mounts)',
        'items': [{
            'desc': 'No',
            'item': 'OFF',
            'elig': 'AE'}, {
            'desc': 'Yes',
            'item': 'ON',
            'elig': 'AE'}]},
    'encoder_count': {
        'desc': 'What is the encoder count?',
        'items': [{
            'desc': 'OFF',
            'item': '0',
            'elig': 'A'}, {
            'desc': 'JTW_24BIT',
            'item': '46603.377778',
            'elig': 'AE'}, {
            'desc': 'JTW_26BIT',
            'item': '186413.511111',
            'elig': 'AE'}, {
            'desc': 'AS37_H39B_B',
            'item': '23301.689',
            'elig': 'PE'}]},
    'driver': {
        'desc': 'What type of drivers does your controller have?',
        'items': [{
            'desc': 'I have a Manticore with no Encoders',
            'item': 'TMC2209',
            'elig': 'M'}, {
            'desc': 'I have a Manticore with encoders',
            'item': 'SERVO_TMC2209',
            'elig': 'ME'}, {
            'desc': 'I have an Original OnStep Controller',
            'item': 'TMC2130_QUIET',
            'elig': 'P'}]},
    'tls': {
        'desc': 'How do you want to manage the clock on your controller?',
        'items': [{
            'desc': 'I want to use the onboard realtime clock. This is the preferred option',
            'item': 'DS3231',
            'elig': 'A'}, {
            'desc': 'I want to use an NTP server, OnStepX will use the hardcoded IP 129.6.15.28 (time-a-g.nist.gov) redefine TIME_IP_ADDR to change this',
            'item': 'NTP',
            'elig': 'M'}, {
            'desc': 'I have a GPS dongle connected to the AUX port. This is not recommended at this time: the GPS can take a long time to obtain a fix and OnStepX will timeout and not retry',
            'item': 'GPS',
            'elig': 'M'}]},
    'pps': {
        'desc': 'Do you want to enable PPS detection? ( this only applies to GPS equipped mounts on the Manticore)',
        'items': [{
            'desc': 'No',
            'item': 'OFF',
            'elig': 'A'}, {
            'desc': 'Yes',
            'item': 'ON',
            'elig': 'MT'}]},
    'pps_detect': {
        'desc': 'Detect the PPS signal on:',
        'items': [{
            'desc': 'OFF',
            'item': 'OFF',
            'elig': 'T'}, {
            'desc': 'Rising signal',
            'item': 'HIGH',
            'elig': 'T'}, {
            'desc': 'Falling signal',
            'item': 'LOW',
            'elig': 'T'}, {
            'desc': 'Both rising and falling signals',
            'item': 'BOTH',
            'elig': 'T'}]},
    'pec_spwr': {
        'desc': 'pec Steps per worm rotation',
        'items': [{
            'desc': 'No PEC sensor',
            'item': '0',
            'elig': 'A'}, {
            'desc': 'GTR with Homing',
            'item': '102400',
            'elig': 'GH'}]},
    'pec_sense': {
        'desc': 'pec sensor config',
        'items': [{
            'desc': 'No PEC sensor',
            'item': 'OFF',
            'elig': 'G'}, {
            'desc': 'GTR defaults',
            'item': 'LOW|THLD(360)|HYST(120)',
            'elig': 'G'}]},
    'home_sense': {
        'desc': 'home sensor config',
        'items': [{
            'desc': 'No Home sensor',
            'item': 'OFF',
            'elig': 'G'}, {
            'desc': 'GTR defaults',
            'item': 'HIGH',
            'elig': 'G'}]},
    'home_switch': {
        'desc': 'home sensor direction configuration display in SWS',
        'items': [{
            'desc': 'Home sensor direction',
            'item': 'OFF',
            'elig': 'G'}, {
            'desc': 'GTR defaults',
            'item': 'ON',
            'elig': 'G'}]},
    'compensation': {
        'desc': 'Do you want to enable tracking compensation (this is configurable at runtime)',
        'items': [{
            'desc': 'No',
            'item': 'OFF',
            'elig': 'A'}, {
            'desc': 'I just want RA refraction compensation (this works best with a TPH probe)',
            'item': 'REFRACTION',
            'elig': 'A'}, {
            'desc': 'I want refraction compensation on both axes (this works best with a TPH probe)',
            'item': 'REFRACTION_DUAL',
            'elig': 'A'}, {
            'desc': 'I just want RA modeling compensation',
            'item': 'MODEL',
            'elig': 'A'}, {
            'desc': 'I want modeling compensation on both axes',
            'item': 'MODEL_DUAL',
            'elig': 'A'}]}
}

# initialize config with the defaults
config = {}
for key, value in choices.items():
    config[key] = value['items'][0]['item']


def print_banner():
    size = os.get_terminal_size()
    banner = 'Welcome to the JTW mount configurator'
    print(textwrap.fill(banner, width=size.columns))
    print(' ')
    banner = ('The script will ask you a series of questions to generate configuration files for OnStepX '
              'and the SmartWebServer.')
    print(textwrap.fill(banner, width=size.columns, initial_indent='  ', subsequent_indent='  '))
    banner = 'you can answer each question by either:'
    print(textwrap.fill(banner, width=size.columns, initial_indent='  ', subsequent_indent='  '))
    banner = '- pressing ENTER to accept the default entry (the first entry in the list)'
    print(textwrap.fill(banner, width=size.columns, initial_indent='    ', subsequent_indent='      '))
    banner = '- typing the number of the entry'
    print(textwrap.fill(banner, width=size.columns, initial_indent='    ', subsequent_indent='      '))
    banner = '- entering a freeform text when required'
    print(textwrap.fill(banner, width=size.columns, initial_indent='    ', subsequent_indent='      '))
    print(' ')
    banner = 'At the end of the process the script will generate 3 files:'
    print(textwrap.fill(banner, width=size.columns, initial_indent='  ', subsequent_indent='  '))
    banner = '- onstepx-Config.h  copy this file as Config.h in your OnStepX repository'
    print(textwrap.fill(banner, width=size.columns, initial_indent='    ', subsequent_indent='      '))
    banner = '- sws-Config.h  copy this file as Config.h in your SWS repository'
    print(textwrap.fill(banner, width=size.columns, initial_indent='    ', subsequent_indent='      '))
    banner = '- sws-Extended.config.h  copy this file as Extended.config.h in your SWS repository'
    print(textwrap.fill(banner, width=size.columns, initial_indent='    ', subsequent_indent='      '))
    print('\n')


def render_menu(menu, eligibility='A', type=None):
    print(' ')
    size = os.get_terminal_size()
    print(textwrap.fill(menu['desc'], width=size.columns))
    index = 1
    items = []
    for item in menu['items']:
        if eligibility in item['elig'] or 'A' in item['elig']:
            print(textwrap.fill(f'{index}. {item['desc']}', width=size.columns, initial_indent='    ', subsequent_indent='       '))
            items.append(index)
        index += 1
    while True:
        response = input('>>> ')
        if not response:
            # empty answer return the default 
            print(textwrap.fill(f'Using default value: {menu['items'][0]['item']}', width=size.columns))
            return menu['items'][0]['item']
        if type == 'choice':
            if response.isnumeric():
                response = int(response)
                if response in items:
                    print(textwrap.fill(f'Using value: {menu['items'][response - 1]['item']}', width=size.columns))
                    return menu['items'][response - 1]['item']
        if type == 'ip':
            response = validate_ip(response)
            if response:
                print(textwrap.fill(f'Using value: {response}', width=size.columns))
                return response
        if type == 'string':
            print(textwrap.fill(f'Using value: {response}', width=size.columns))
            return response
        print('Invalid choice, try again')


def validate_ip(ip):
    match = re.search(r'\{\b(?:\d{1,3},){3}\d{1,3}\b\}', ip)
    if match:
        return ip
    else:
        match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', ip)
        if match:
            nums = ip.split('.')
            return '{' + f'{nums[0]},{nums[1]},{nums[2]},{nums[3]}' + '}'
        else:
            return None


def top_level():
    config['model'] = render_menu(choices['model'], type='choice')
    config['board'] = render_menu(choices['board'], type='choice')
    # config['temp'] = render_menu(choices['temp'], type='choice')
    # config['weather'] = render_menu(choices['weather'], type='choice')
    config['compensation'] = render_menu(choices['compensation'], type='choice')
    if config['model'] == 'GTR':
        config['encoder'] = render_menu(choices['encoder'], 'G', type='choice')
        if config['encoder'] == 'OFF':
            # GTRs without encoders have PEC and Home sensors
            print('Configuring your GTR with homing and PEC sensors...')
            config['options'] += 'H P '
            config['pec_spwr'] = choices['pec_spwr']['items'][1]['item']
            config['pec_sense'] = choices['pec_sense']['items'][1]['item']
            config['home_sense'] = choices['home_sense']['items'][1]['item']
            config['home_switch'] = choices['home_switch']['items'][1]['item']
    if config['model'] == 'P75':
        config['encoder'] = render_menu(choices['encoder'], 'P', type='choice')
        if config['encoder'] == 'AS37_H39B_B':
            config['encoder_reverse'] = 'ON'
    if config['board'] == 'MANTICORE':
        set_wifi_mode(render_menu(choices['wifi_mode'], 'M', type='choice'))
        config['eth_dhcp'] = render_menu(choices['eth_dhcp'], 'M', type='choice')
        if config['eth_dhcp'] == 'false':
            config['eth_ip'] = render_menu(choices['eth_ip'], 'M', 'ip')
            config['eth_mask'] = render_menu(choices['eth_mask'], 'M', 'ip')
            config['eth_gw'] = render_menu(choices['eth_gw'], 'M', 'ip')
        config['weather_mode'] = render_menu(choices['weather_mode'], 'M', type='choice')
        config['tls'] = render_menu(choices['tls'], 'M', type='choice')
        if config['tls'] == 'GPS':
            config['pps'] = render_menu(choices['pps'], 'T', type='choice')
            if config['pps'] == 'ON':
                config['pps_detect'] = render_menu(choices['pps_detect'], 'T', type='choice')
    else:
        set_wifi_mode(render_menu(choices['wifi_mode'], type='choice'))
        # if config['wifi_mode'] == 'WIFI_STATION':
        #     config['tls'] = render_menu(choices['tls'], 'S', type='choice')

    # infered configs
    # encoder counts
    for counts in choices['encoder_count']['items']:
        if counts['desc'] == config['encoder']:
            config['encoder_count'] = counts['item']
    # drivers
    if config['board'] == 'MANTICORE':
        if config['encoder'] != 'OFF':
            config['driver'] = choices['driver']['items'][1]['item']
        else:
            config['driver'] = choices['driver']['items'][0]['item']
    else:
        config['driver'] = choices['driver']['items'][2]['item']
    # servo display options
    if config['driver'] == choices['driver']['items'][1]['item']:
        config['monitor'] = 'ON'
        config['origin'] = 'ON'
        config['calibration'] = 'ON'
    # option string
    if config['encoder'] == 'JTW_24BIT':
        config['options'] += '24b '
    if config['encoder'] == 'JTW_26BIT':
        config['options'] += '26b '
    if config['encoder'] == 'AS37_H39B_B':
        config['options'] += '23b '
    if config['tls'] == 'GPS':
        config['options'] += 'GPS '
    if config['tls'] == 'NTP':
        config['options'] += 'NTP '
    if config['weather_mode'] == 'BME280_0x76':
        config['options'] += 'TPH '


def set_wifi_mode(mode):
    if mode == 'WIFI_ACCESS_POINT':
        config['ap_enabled'] = 'true'
        config['sta_enabled'] = 'false'
        config['wifi_mode'] = 'WIFI_ACCESS_POINT'
        config['options'] += 'Wa '
        config['ap_ssid'] = render_menu(choices['ap_ssid'], type='string')
        config['ap_password'] = render_menu(choices['ap_password'], type='string')
        config['ap_wifi_ip'] = render_menu(choices['ap_wifi_ip'], type='ip')
        config['ap_wifi_mask'] = render_menu(choices['ap_wifi_mask'], type='ip')
    elif mode == 'WIFI_STATION':
        config['ap_enabled'] = 'false'
        config['sta_enabled'] = 'true'
        config['wifi_mode'] = 'WIFI_STATION'
        config['options'] += 'Ws '
        config['sta_ssid'] = render_menu(choices['sta_ssid'], type='string')
        config['sta_password'] = render_menu(choices['sta_password'], type='string')
        config['wifi_dhcp'] = render_menu(choices['wifi_dhcp'], type='choice')
        if config['wifi_dhcp'] == 'false':
            config['sta_wifi_ip'] = render_menu(choices['sta_wifi_ip'], type='ip')
            config['sta_wifi_mask'] = render_menu(choices['sta_wifi_mask'], type='ip')
            config['sta_wifi_gw'] = render_menu(choices['sta_wifi_gw'], type='ip')
    elif mode == 'BLUETOOTH':
        config['ap_enabled'] = 'false'
        config['sta_enabled'] = 'false'
        config['wifi_mode'] = 'BLUETOOTH'
        config['options'] += 'Bt '
    else:
        config['ap_enabled'] = 'false'
        config['sta_enabled'] = 'false'
        config['wifi_mode'] = 'OFF'


def render_files():
    if config['board'] == 'MANTICORE':
        suffix = 'manticore'
    else:
        suffix = 'legacy'

    # print(config)

    with open(f'Config.onstepx.{suffix}', 'r', encoding='utf-8') as fr:
        src = Template(fr.read())
        result = src.substitute(config)
    with open('onstepx-Config.h', 'w', encoding='utf-8') as fw:
        fw.write(result)

    with open(f'Config.sws.{suffix}', 'r', encoding='utf-8') as fr:
        src = Template(fr.read())
        result = src.substitute(config)
    with open('sws-Config.h', 'w', encoding='utf-8') as fw:
        fw.write(result)

    with open(f'Extended.config.sws.{suffix}', 'r', encoding='utf-8') as fr:
        src = Template(fr.read())
        result = src.substitute(config)
    with open('sws-Extended.config.h', 'w', encoding='utf-8') as fw:
        fw.write(result)


def signal_handler(sig, frame):
    print('Aborted, Exiting...')
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    print_banner()
    top_level()
    render_files()
