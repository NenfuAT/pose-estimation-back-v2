package usecase

import "pose-estimation/application/service"

type PoseEstimationUseCase interface {
	// EstimationQuaternion()
	// EstimationDistance()
	EstimatePose()
}

type poseEstimationUseCase struct {
	service service.PoseEstimationService
}

func NewPoseEstimationUseCase(service service.PoseEstimationService) PoseEstimationUseCase {
	return &poseEstimationUseCase{service}
}

// func (u *poseEstimationUseCase) EstimationQuaternion() {
// 	//u.service.CalculateQuaternion()
// 	panic("unimplemented")
// }

// EstimatePose implements PoseEstimationUseCase.
func (u *poseEstimationUseCase) EstimatePose() {
	panic("unimplemented")
}

// // EstimationDistance implements PoseEstimationUseCase.
// func (u *poseEstimationUseCase) EstimationDistance() {
// 	panic("unimplemented")
// }
