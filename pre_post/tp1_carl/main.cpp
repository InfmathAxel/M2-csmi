#include <vtkActor.h>
#include <vtkCamera.h>
#include <vtkCylinderSource.h>
#include <vtkNamedColors.h>
#include <vtkPolyDataMapper.h>
#include <vtkProperty.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkRenderer.h>
#include <vtkSmartPointer.h>
#include <vtkUnstructuredGrid.h>
#include <vtkCellType.h>
#include <vtkDataSetMapper.h>
#include <vtkInteractorStyleTrackballCamera.h>
#include <string>
#include <iostream>
#include <cmath>

class CustomInteractor : public vtkInteractorStyleTrackballCamera {
public:
    static CustomInteractor* New();
    void OnKeyPress() override;
};

vtkStandardNewMacro(CustomInteractor);

void CustomInteractor::OnKeyPress() {
    std::string key = this->Interactor->GetKeySym();  // Use this->Interactor to get the key
    vtkRenderer* currentRenderer = this->GetCurrentRenderer();
    
    if (currentRenderer->GetActors()->GetNumberOfItems() > 0) {

        vtkActor* actor = currentRenderer->GetActors()->GetLastActor();  // Get the actor
        
        vtkProperty* property = actor->GetProperty();
        double Opacity = property->GetOpacity();

        if (key == "Up") {
            std::cout << "Up key pressed" << std::endl;
            property->SetOpacity(std::min(1., Opacity + 0.05));
        }
        if (key == "Down") {
            std::cout << "Down key pressed" << std::endl;
            property->SetOpacity(std::max(0., Opacity - 0.05));
        }
        if (key == "w"){
            std::cout << "w key pressed" << std::endl;
            property->SetRepresentationToWireframe();
        }
        if (key == "s"){
            std::cout << "s key pressed" << std::endl;
            property->SetRepresentationToSurface();
        }
        
        currentRenderer->GetRenderWindow()->Render();  // Refresh the window
    }
    
    // Call the base class method to handle other key events, such as camera movement
    vtkInteractorStyle::OnKeyPress();
}

int main(int argc, const char *argv[]) {

    vtkSmartPointer<vtkPoints> pointSet = vtkSmartPointer<vtkPoints>::New();
    vtkSmartPointer<vtkIdList> listSet_1 = vtkSmartPointer<vtkIdList>::New();
    vtkSmartPointer<vtkIdList> listSet_2 = vtkSmartPointer<vtkIdList>::New();
    vtkSmartPointer<vtkUnstructuredGrid> grid = vtkSmartPointer<vtkUnstructuredGrid>::New();

    vtkSmartPointer<vtkRenderer> renderer = vtkSmartPointer<vtkRenderer>::New();
    vtkSmartPointer<vtkDataSetMapper> mapper = vtkSmartPointer<vtkDataSetMapper>::New();
    vtkSmartPointer<vtkActor> actor = vtkSmartPointer<vtkActor>::New();

    vtkSmartPointer<vtkRenderWindow> renderWindow = vtkSmartPointer<vtkRenderWindow>::New();
    vtkSmartPointer<vtkRenderWindowInteractor> renderWindowInteractor = vtkSmartPointer<vtkRenderWindowInteractor>::New();

    vtkSmartPointer<CustomInteractor> style = vtkSmartPointer<CustomInteractor>::New();
    renderWindowInteractor->SetInteractorStyle(style);

    pointSet->InsertNextPoint(0, 0, 1);
    pointSet->InsertNextPoint(0, 1, 0);
    pointSet->InsertNextPoint(1, 0, 0);
    pointSet->InsertNextPoint(0, 0, 0);
    pointSet->InsertNextPoint(1, 1, -1);

    listSet_1->InsertNextId(0);
    listSet_1->InsertNextId(1);
    listSet_1->InsertNextId(2);
    listSet_1->InsertNextId(3);

    listSet_2->InsertNextId(1);
    listSet_2->InsertNextId(2);
    listSet_2->InsertNextId(3);
    listSet_2->InsertNextId(4);

    grid->SetPoints(pointSet);

    vtkIdType ids_1[4] = {0, 1, 2, 3};
    grid->InsertNextCell(VTK_TETRA, 4, ids_1);

    vtkIdType ids_2[4] = {1, 2, 3, 4};
    grid->InsertNextCell(VTK_TETRA, 4, ids_2);

    mapper->SetInputData(grid);
    actor->SetMapper(mapper);
    renderer->AddActor(actor);
    renderWindow->AddRenderer(renderer);

    renderWindowInteractor->SetRenderWindow(renderWindow);
    
    renderWindow->Render();

    renderWindowInteractor->Start();

    return 0;
}