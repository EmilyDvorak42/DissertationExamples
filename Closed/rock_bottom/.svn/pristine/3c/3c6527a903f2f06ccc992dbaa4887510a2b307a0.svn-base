/**
 * copyright  (C) 2010
 * The Icecube Collaboration
 *
 * $Id: SnowCorrectionDiagnostics.cxx 173671 2019-06-03 17:59:13Z acoleman $
 *
 * @version $Revision: 173671 $
 * @date $Date: 2019-06-03 12:59:13 -0500 (Mon, 03 Jun 2019) $
 * @author Katherine Rawlins <krawlins@uaa.alaska.edu>
 */

#include <icetray/serialization.h>
#include "rock_bottom/snowservices/SnowCorrectionDiagnostics.h" 


// ---------- SERIALIZATION ---------------
template <class Archive>
void I3ComboSnowCorrectionDiagnostics::serialize(Archive& ar, unsigned version)
{
  ar & make_nvp("I3FrameObject", base_object<I3FrameObject>(*this));
  // The stage of shower evolution
  ar & make_nvp("tstage", tstage);
  ar & make_nvp("tstage_restricted", tstage_restricted);
  
  // Fraction of signal which is EM
  ar & make_nvp("fEM_30m", fEM_30m);
  ar & make_nvp("fEM_50m", fEM_50m);
  ar & make_nvp("fEM_80m", fEM_80m);
  ar & make_nvp("fEM_100m", fEM_100m);
  ar & make_nvp("fEM_125m", fEM_125m);
  ar & make_nvp("fEM_150m", fEM_150m);
  ar & make_nvp("fEM_200m", fEM_200m);
  ar & make_nvp("fEM_300m", fEM_300m);
  ar & make_nvp("fEM_500m", fEM_500m);
  ar & make_nvp("fEM_1000m", fEM_1000m);

  // Effective lambda's: EM only
  ar & make_nvp("lambda_EM_30m", lambda_EM_30m);
  ar & make_nvp("lambda_EM_50m", lambda_EM_50m);
  ar & make_nvp("lambda_EM_80m", lambda_EM_80m);
  ar & make_nvp("lambda_EM_100m", lambda_EM_100m);
  ar & make_nvp("lambda_EM_125m", lambda_EM_125m);
  ar & make_nvp("lambda_EM_150m", lambda_EM_150m);
  ar & make_nvp("lambda_EM_200m", lambda_EM_200m);
  ar & make_nvp("lambda_EM_300m", lambda_EM_300m);
  ar & make_nvp("lambda_EM_500m", lambda_EM_500m);
  ar & make_nvp("lambda_EM_1000m", lambda_EM_1000m);
  ar & make_nvp("lambda_EM_30m_restricted", lambda_EM_30m_restricted);
  ar & make_nvp("lambda_EM_50m_restricted", lambda_EM_50m_restricted);
  ar & make_nvp("lambda_EM_80m_restricted", lambda_EM_80m_restricted);
  ar & make_nvp("lambda_EM_100m_restricted", lambda_EM_100m_restricted);
  ar & make_nvp("lambda_EM_125m_restricted", lambda_EM_125m_restricted);
  ar & make_nvp("lambda_EM_150m_restricted", lambda_EM_150m_restricted);
  ar & make_nvp("lambda_EM_200m_restricted", lambda_EM_200m_restricted);
  ar & make_nvp("lambda_EM_300m_restricted", lambda_EM_300m_restricted);
  ar & make_nvp("lambda_EM_500m_restricted", lambda_EM_500m_restricted);
  ar & make_nvp("lambda_EM_1000m_restricted", lambda_EM_1000m_restricted);

  /* not yet
  ar & make_nvp("lambda_eff_30m", lambda_eff_30m);
  ar & make_nvp("lambda_eff_50m", lambda_eff_50m);
  ar & make_nvp("lambda_eff_80m", lambda_eff_80m);
  ar & make_nvp("lambda_eff_100m", lambda_eff_100m);
  ar & make_nvp("lambda_eff_125m", lambda_eff_125m);
  ar & make_nvp("lambda_eff_150m", lambda_eff_150m);
  ar & make_nvp("lambda_eff_200m", lambda_eff_200m);
  ar & make_nvp("lambda_eff_300m", lambda_eff_300m);
  ar & make_nvp("lambda_eff_500m", lambda_eff_500m);
  ar & make_nvp("lambda_eff_1000m", lambda_eff_1000m);
  */
}

I3_SERIALIZABLE(I3ComboSnowCorrectionDiagnostics);  // <--- has to be in a .cxx, not an .h

