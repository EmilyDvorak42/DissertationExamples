#!/usr/bin/env python
from icecube.rock_bottom import I3ParameterMap
from icecube import tableio

class I3ParameterMapConverter(tableio.I3Converter):
    booked = I3ParameterMap
    def CreateDescription(self, pamparams):
        desc = tableio.I3TableRowDescription()
        desc.add_field('Log10_S125',tableio.types.Float64, '', 
                       'Logarithmic signal strength at 125m from shower core.')
        desc.add_field('Beta',tableio.types.Float64, '', 
                       'Beta.')
        desc.add_field('RhoMu',tableio.types.Float64, '', 
                       'Muon LDF signal strength at r_mu_ref.')
        desc.add_field('Chi2_ldf',tableio.types.Float64, '', 
                       'Chi2 from LDF fit.')
        desc.add_field('ndof_ldf',tableio.types.Float64, '', 
                       'Number of degrees of freedom from LDF fit.')
        desc.add_field('r_ref',tableio.types.Float64, '', 
                       'Distance reference.')
        desc.add_field('Moliere',tableio.types.Float64, '', 
                       'Moliere radius.')
        desc.add_field('r_mu_ref',tableio.types.Float64, '', 
                       'Distance reference for muon LDF only.')
        desc.add_field('llh_ldf',tableio.types.Float64, '', 
                       'Likelihood LDF.')
        desc.add_field('LDFtype',tableio.types.Float64, '', 
                       'Flag for DLP/NKG.')
        desc.add_field('gamma',tableio.types.Float64, '', 
                       'Zenith dependent parameter for muon LDF.')
        desc.add_field('omega',tableio.types.Float64, '', 
                       'Zenith dependent parameter for muon LDF.')
        desc.add_field('Amp',tableio.types.Float64, '', 
                       'Curvature amplitude.')
        desc.add_field('Chi2_time',tableio.types.Float64, '', 
                       'Chi2 from LDF time fit.')
        desc.add_field('ndof_time',tableio.types.Float64, '', 
                       'Number of degrees of freedom for time fit.')
        desc.add_field('llh_time',tableio.types.Float64, '', 
                       'Likelihood from time fit.')
        desc.add_field('NX',tableio.types.Float64, '', 
                       'Normalized X direction.')
        desc.add_field('NY',tableio.types.Float64, '', 
                       'Normalized Y direction.')
        desc.add_field('Kappa',tableio.types.Float64, '', 
                       'DLP parameter.')
        desc.add_field('Dcurve',tableio.types.Float64, '', 
                       'Width of exponential nose of shower front..')
        desc.add_field('Ncurve',tableio.types.Float64, '', 
                       'Normalization in exponential nose of shower front.')
        desc.add_field('ndof',tableio.types.Float64, '', 
                       'Number of degrees of freedom.')
        return desc

    def FillRows(self, pamparams, rows):
        rows['Log10_S125']  = pamparams['Log10_S125']
        rows['Beta']        = pamparams['Beta']
        rows['RhoMu']       = pamparams['RhoMu']
        rows['Chi2_ldf']    = pamparams['Chi2_ldf']
        rows['ndof_ldf'] = pamparams['ndof_ldf']
        rows['r_ref'] = pamparams['r_ref']
        rows['Moliere'] = pamparams['Moliere']
        rows['r_mu_ref'] = pamparams['r_mu_ref']
        rows['llh_ldf'] = pamparams['llh_ldf']
        rows['LDFtype'] = pamparams['LDFtype']
        rows['gamma'] = pamparams['gamma']
        rows['omega'] = pamparams['omega']
        rows['Amp'] = pamparams['Amp']
        rows['Chi2_time'] = pamparams['Chi2_time']
        rows['ndof_time'] = pamparams['ndof_time']
        rows['llh_time'] = pamparams['llh_time']
        rows['NX'] = pamparams['NX']
        rows['NY'] = pamparams['NY']
        rows['Kappa'] = pamparams['Kappa']
        rows['Dcurve'] = pamparams['Dcurve']
        rows['Ncurve'] = pamparams['Ncurve']
        rows['ndof'] = pamparams['ndof']
        
        return 1


tableio.I3ConverterRegistry.register(I3ParameterMapConverter)
