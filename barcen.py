from astropy.coordinates import SkyCoord, EarthLocation
from astropy import units as u, constants as c
from astropy.time import Time
import numpy as np
from scipy.interpolate import interp1d

telescope_location = EarthLocation(lat=52.812162*u.deg, lon=6.3963282*u.deg, height=35*u.m)
dt = 512*64/70e6

def barcen_freqs(pulsar, freqs, obs_time_middle):
    """Corrects for the first order redshift because of the barycentric motion of the earth
    
    pulsar -- the pulsar object that will be used for the location of the pulsar
    freqs -- The array with the observed frequencies
    obsmiddle -- the datetime of the middle of the observation as astropy Time object (let's keep things simple for the moment, and not consider changing frequencies etc...)

    Returns:
    The frequencies that would have been observed at the SSB
    """
    pulsar_loc = SkyCoord(ra=pulsar.RAJD*u.deg, dec=pulsar.DECJD*u.deg)
    vel_cor = pulsar_loc.radial_velocity_correction(kind='barycentric', obstime=obs_time_middle, location=telescope_location)
    return freqs/(1+(vel_cor/c.c).to_value(1))

def barcen_times(pulsar, obs_duration, obsstart=Time.now()):
    """Calculates the times that photons would have arrived at the solar system Barycenter
    
    Arguments:
    pulsar -- the pulsar object that will be used for the location of the pulsar
    obsstart -- the datetime of the object, in isot format, or as astropy Time object
    obs_duration -- the observation time in units of dt, so just len(data_array)

    Returns:
    corrected time array of length obs_duration
    """
    obsstart = Time(obsstart)
    time_array = dt * np.arange(obs_duration)
    pulsar_loc = SkyCoord(ra=pulsar.RAJD*u.deg, dec=pulsar.DECJD*u.deg)
    corr = lambda time: time.light_travel_time(pulsar_loc, location=telescope_location).to(u.s).value
    corrafterobs = lambda t: corr(obsstart + t*u.s) - corr(obsstart)
    int_sample_t = obs_duration*dt*np.linspace(0,1,5)
    int_func = interp1d(int_sample_t, corrafterobs(int_sample_t))
    corrs_int = int_func(time_array.copy())
    return time_array + corrs_int
