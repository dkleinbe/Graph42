#include "app.h"
#include <log4cplus/consoleappender.h>
#include <log4cplus/loggingmacros.h>
#include <log4cplus/configurator.h>

#include "MainWindow.h"

using namespace std;
using namespace log4cplus;

int main(int argc, char* argv[])
{
	Logger logger = Logger::getRoot();
	log4cplus::initialize ();
	try {
		PropertyConfigurator::doConfigure(LOG4CPLUS_TEXT("log4cplus.properties"));

		LOG4CPLUS_WARN(logger, "Log enabled");
   
	}
	catch(...) {
		cout << "Exception..." << endl;
		LOG4CPLUS_FATAL(logger, "Exception occured...");
	}
	
	App app(argc,argv);
	MainWindow w;
	w.show();

	return app.exec();
}

