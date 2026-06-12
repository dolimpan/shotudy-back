from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class UserLevelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "current_level": request.user.current_level
        })

    def patch(self, request):
        level = request.data.get("current_level")

        if level is None:
            return Response(
                {"error": "current_level is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.current_level = level
        request.user.save()

        return Response({
            "current_level": request.user.current_level
        })