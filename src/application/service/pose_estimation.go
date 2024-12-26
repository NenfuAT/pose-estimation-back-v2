package service

type PoseEstimationService interface {
	CalculateQuaternion()
	CalculateDistance()
}

type poseEstimationService struct {
	repo repository.PoseEstimationRepository
}

func NewPoseEstimationService(repo repository.PoseEstimationRepository) PoseEstimationService {
	return &poseEstimationService{repo}
}
