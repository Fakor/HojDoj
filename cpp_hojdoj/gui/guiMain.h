/***************************************************************
 * Name:      guiMain.h
 * Purpose:   Defines Application Frame
 * Author:     ()
 * Created:   2019-11-03
 * Copyright:  ()
 * License:
 **************************************************************/

#ifndef GUIMAIN_H
#define GUIMAIN_H

#ifndef WX_PRECOMP
    #include <wx/wx.h>
#endif

#include "guiApp.h"

class guiFrame: public wxFrame
{
    public:
        guiFrame(wxFrame *frame, const wxString& title);
        ~guiFrame();
    private:
        enum
        {
            idMenuQuit = 1000,
            idMenuAbout
        };
        void OnClose(wxCloseEvent& event);
        void OnQuit(wxCommandEvent& event);
        void OnAbout(wxCommandEvent& event);
        DECLARE_EVENT_TABLE()
};


#endif // GUIMAIN_H
