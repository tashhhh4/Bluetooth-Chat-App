from jnius import autoclass

PythonActivity = autoclass('org.kivy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')

def turn_discoverability_on():
    activity = PythonActivity.mActivity
    intent = Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE)
    intent.putExtra(BluetoothAdapter.EXTRA_DISCOVERABLE_DURATION, 300)

    activity.startActivity(intent)


def turn_scanning_on():
    print('We want to turn Bluetooth scanning on! (Not yet implemented')

def turn_scanning_off():
    print('We want to turn Bluetooth scanning off! (Not yet implemented)')