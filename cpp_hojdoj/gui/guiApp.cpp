/***************************************************************
 * Name:      guiApp.cpp
 * Purpose:   Code for Application Class
 * Author:     ()
 * Created:   2019-11-03
 * Copyright:  ()
 * License:
 **************************************************************/

#ifdef WX_PRECOMP
#include "wx_pch.h"
#endif

#ifdef __BORLANDC__
#pragma hdrstop
#endif //__BORLANDC__

#include "guiApp.h"
#include "guiMain.h"

IMPLEMENT_APP(guiApp);

bool guiApp::OnInit()
{
    guiFrame* frame = new guiFrame(0L, _("wxWidgets Application Template"));
    
    frame->Show();
    
    return true;
}
