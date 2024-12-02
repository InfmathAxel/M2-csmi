#include <iostream>
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
#include <vtkDataSetMapper.h>

#include <array>

int main()
{
    std::cout << "Hello world je susimes pas cooked" << std::endl;

    vtkPoints *pointSet_ = NULL;
    pointSet_ = vtkPoints::New();
    
    vtkIdList *idList_ = NULL;
    idList_= vtkIdList::New();

    vtkUnstructuredGrid *grid_ = NULL;
    grid_ = vtkUnstructuredGrid::New();


    (*pointSet_).InsertNextPoint(0,0,1);
    (*pointSet_).InsertNextPoint(0,1,0);
    (*pointSet_).InsertNextPoint(1,0,0);
    (*pointSet_).InsertNextPoint(0,0,0);
    (*pointSet_).InsertNextPoint(0,0,-1);
    
    (*idList_).InsertNextId(0);
    (*idList_).InsertNextId(1);
    (*idList_).InsertNextId(2);
    (*idList_).InsertNextId(3);
    
    vtkIdType ids[4];
    ids[0] = idList_->GetId(0);
    ids[1] = idList_->GetId(1);
    ids[2] = idList_->GetId(2);
    ids[3] = idList_->GetId(3);

    (*grid_).SetPoints(pointSet_);
    (*grid_).InsertNextCell(VTK_TETRA,4,ids);


    vtkSmartPointer<vtkRenderer> renderer = vtkSmartPointer<vtkRenderer>::New();
    vtkSmartPointer<vtkActor> Actor = vtkSmartPointer<vtkActor>::New();
    vtkSmartPointer<vtkDataSetMapper> mapper = vtkSmartPointer<vtkDataSetMapper>::New();
    vtkSmartPointer<vtkNamedColors> colors =vtkSmartPointer<vtkNamedColors>::New();

    std::array<unsigned char, 4> bkg{{26, 51, 102, 255}};
    colors->SetColor("BkgColor", bkg.data());
    mapper->SetInputData(grid_);
    Actor->SetMapper(mapper);

    renderer->AddActor(Actor);
    renderer->SetBackground(colors->GetColor3d("BkgColor").GetData());
    // Zoom in a little by accessing the camera and invoking its "Zoom" method.
    renderer->ResetCamera();
    renderer->GetActiveCamera()->Zoom(1.5);

    // The render window is the actual GUI window
    // that appears on the computer screen
    vtkSmartPointer<vtkRenderWindow> renderWindow =
    vtkSmartPointer<vtkRenderWindow>::New();
    renderWindow->SetSize(1920, 1080);
    renderWindow->AddRenderer(renderer);
   

    vtkSmartPointer<vtkRenderWindowInteractor> renderWindowInteractor =
      vtkSmartPointer<vtkRenderWindowInteractor>::New();
    renderWindowInteractor->SetRenderWindow(renderWindow);

    // This starts the event loop and as a side effect causes an initial render.
    renderWindow->Render();
    renderWindowInteractor->Start();   


    (*pointSet_).Delete();
    (*idList_).Delete();
    (*grid_).Delete();
    return 0;
}