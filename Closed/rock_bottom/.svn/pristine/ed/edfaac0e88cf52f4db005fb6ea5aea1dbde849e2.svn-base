//This is the cluster of objects that get passed to the signal
//model likelihood functions.


#ifndef _rock_bottom_I3RockBall_h_
#define _rock_bottom_I3RockBall_h_

#include <rock_bottom/I3ParameterMap.h>
#include <dataclasses/geometry/I3TankGeo.h>
#include <dataclasses/geometry/I3OMGeo.h>
#include <dataclasses/calibration/I3VEMCalibration.h>

class I3RockBall {
 public:

  I3RockBall();
  I3RockBall(const I3RockBall &ball);
  ~I3RockBall() {}

  void SetTankGeo(const I3TankGeo *tankGeo);
  const I3TankGeo* GetTankGeo() const;

  void SetVEMCalibration(const I3VEMCalibration *vemCalib);
  const I3VEMCalibration* GetVEMCalibration() const;

  void SetPosition(const I3Position *pos);
  const I3Position* GetPosition() const;

  void SetSaturatedStatus(bool x);
  const bool GetSaturatedStatus() const;

  void SetCharge(double x);
  const double GetCharge() const;

  void SetCharge2(double x);
  const double GetCharge2() const;

  void SetDeltaT(double x);
  const double GetDeltaT() const;

  void SetDeltaT2(double x);
  const double GetDeltaT2() const;

 private:
  const I3TankGeo *tankGeo_;
  const I3VEMCalibration *vemCalib_;
  const I3Position *pos_;

  bool saturated_;
  double charge_;
  double charge2_;
  double deltaT_;
  double deltaT2_;
};

#endif
