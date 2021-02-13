#include <rock_bottom/interface/I3RockBall.h>

#include <icetray/I3Logging.h>

I3RockBall::I3RockBall() {
  tankGeo_ = NULL;
  vemCalib_ = NULL;
  pos_ = NULL;

  saturated_ = false;
  charge_ = NAN;
  deltaT_ = NAN;
}

I3RockBall::I3RockBall(const I3RockBall &ball) {
  tankGeo_ = ball.tankGeo_;
  vemCalib_ = ball.vemCalib_;
  pos_ = ball.pos_;

  saturated_ = ball.saturated_;
  charge_ = ball.charge_;
  deltaT_ = ball.deltaT_;
}


void I3RockBall::SetTankGeo(const I3TankGeo *tankGeo) {
  tankGeo_ = tankGeo;
}
const I3TankGeo* I3RockBall::GetTankGeo() const {
  if (NULL == tankGeo_) {
    log_warn("You are asking for a TankGeo that does not exist!");
  }
  return tankGeo_;
}


void I3RockBall::SetVEMCalibration(const I3VEMCalibration *vemCalib) {
  vemCalib_ = vemCalib;
}
const I3VEMCalibration* I3RockBall::GetVEMCalibration() const {
  if (NULL == vemCalib_) {
    log_warn("You are asking for a VEMCalibration that does not exist!");
  }
  return vemCalib_;
}


void I3RockBall::SetPosition(const I3Position *pos) {
  pos_ = pos;
}
const I3Position* I3RockBall::GetPosition() const {
  if (NULL == pos_) {
    log_warn("You are asking for a Position that does not exist!");
  }
  return pos_;
}


void I3RockBall::SetSaturatedStatus(bool x) {
  saturated_ = x;
}
const bool I3RockBall::GetSaturatedStatus() const {
  return saturated_;
}


void I3RockBall::SetCharge(double x) {
  charge_ = x;
}
const double I3RockBall::GetCharge() const {
  if (NAN == charge_) {
    log_warn("You are asking for a charge that has not been set!");
  }
  return charge_;
}
void I3RockBall::SetCharge2(double x) {
  charge2_ = x;
}
const double I3RockBall::GetCharge2() const {
  if (NAN == charge2_) {
    log_warn("You are asking for a charge that has not been set!");
  }
  return charge2_;
}

void I3RockBall::SetDeltaT(double dt) {
  deltaT_ = dt;
}
const double I3RockBall::GetDeltaT() const {
  if (NAN == deltaT_) {
    log_warn("You are asking for a time that has not been set!");
  }
  return deltaT_;
}
void I3RockBall::SetDeltaT2(double dt2) {
  deltaT2_ = dt2;
}
const double I3RockBall::GetDeltaT2() const {
  if (NAN == deltaT2_) {
    log_warn("You are asking for a time that has not been set!");
  }
  return deltaT2_;
}

