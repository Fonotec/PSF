import camrasdevices

my_receiver = camrasdevices.Receiver

my_receiver.frequency = 405e6

# or with units:
import astropy.units as u

my_receiver.frequency = 405 * u.MHz





import telescope

my_telescope = telescope(consoleHost='console')

my_telescope.getRaDec()
