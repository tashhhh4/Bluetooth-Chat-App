from jnius import autoclass

PythonActivity = autoclass('org.kivy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')

def turn_discoverability_on():
    activity = PythonActivity.mActivity
    intent = Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE)
    intent.putExtra(BluetoothAdapter.EXTRA_DISCOVERABLE_DURATION, 300)

    activity.startActivity(intent)
