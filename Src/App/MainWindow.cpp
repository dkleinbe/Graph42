#include "MainWindow.h"
#include "ui_GraphItApp.h"
#include <QMessageBox>
#include <QCloseEvent>
#include <QtWebKitWidgets>

#include <tchar.h>

#include "RestGraphDatabaseLib/RestGraphDatabase.h"
#include "RestGraphDatabaseLib/Neo4JRestAPI.h"
#include "RestGraphDatabaseLib/Node.h"

#include "MyLoggingMacros.h"

using namespace log4cplus;
static Logger logger = Logger::getRoot();

MainWindow::MainWindow() : QMainWindow(NULL), _ui(new Ui::MainWindowUi) // 1.
{
	//
	// setup UI
	//
	_ui->setupUi(this);
	//
	// Redictect wcout to log window
	//
	_coutStream = new StreamRedirector<wchar_t>(std::wcout, _ui->textEditLog);
	//
	//
	//
	//_ui->webViewGraph->load(QUrl("hgj"));

	QFile file;
	
	file.setFileName(":/GraphIt/Resources/vivagraph.min.js");
	file.open(QIODevice::ReadOnly);
	_vivaGraph = file.readAll();
	file.close();

	file.setFileName("./vivagraph.custom.js");
	file.open(QIODevice::ReadOnly);
	_vivaGraphCustom = file.readAll();
	file.close();

	_ui->webViewGraph->page()->mainFrame()->evaluateJavaScript(_vivaGraph);
	_ui->webViewGraph->page()->mainFrame()->evaluateJavaScript(_vivaGraphCustom);

	QString aze;
	aze = "{ var graph = Viva.Graph.graph(); var renderer = Viva.Graph.View.renderer(graph); renderer.run(); }";
	
	//_ui->webViewGraph->page()->mainFrame()->evaluateJavaScript(aze);

	LOG4CPLUS_INFO(logger, LOG4CPLUS_TEXT("GraphIt started !")); // 
	LOG4CPLUS_WARN(logger, "Log started");

	connect(_ui->actionConnect, SIGNAL(triggered()), this, SLOT(Connect()) /*, Qt::QueuedConnection */);
	//connect(_ui->actionExit, SIGNAL(toggled(bool)), this, SLOT(close()));

	//connect(_ui->webViewGraph, SIGNAL(loadFinished(bool)), SLOT(FinishLoading(bool)));
}
/*!
 * \deprecated Not used
 */
void
MainWindow::FinishLoading(bool)
{
	//_ui->webViewGraph->page()->mainFrame()->evaluateJavaScript(_vivaGraph);

	//QString aze;
	//aze = "var graph = Viva.Graph.graph(); graph.addLink(1, 2); var renderer = Viva.Graph.View.renderer(graph); renderer.run();";
	//aze = "var graph = Viva.Graph.graph(); var renderer = Viva.Graph.View.renderer(graph); renderer.run();";
	
	//_ui->webViewGraph->page()->mainFrame()->evaluateJavaScript(aze);

}
/*!
 *
 */
void
MainWindow::Connect()
{
	Neo4JRestAPI restApi;
	Node *aNode;
	Relationship *aRel;
	RelationshipList relList;

	restApi.GetServiceRoot();
	aNode = restApi.GetNodeById(3);
	LOG_TRACE("Node version: " + aNode->GetProperty("version"));

	relList = aNode->GetRelationships();
	aNode = relList[1]->GetEndNode();
	Relationship *rel = relList[1];

	LOG_TRACE("Relation type: " + rel->GetType());
	LOG_TRACE("Relation property[stars]: " + rel->GetProperty("stars"));
	//restApi.GetNodeById(340000);
	aRel = restApi.GetRelationshipById(632);

	QString relGraphString;
	NodePair nodes(aRel->GetNodes());

	relGraphString.append(tr("graph.addLink(\"%1\", \"%2\"); ").arg(nodes.first->GetId()).arg(nodes.second->GetId()));
	
	for (int i = 0 ; i < relList.size() ; i++)
	{
		relGraphString.append(tr("graph.addLink(\"%1\", \"%2\"); ").arg(relList[i]->GetStartNode()->GetId()).arg(relList[i]->GetEndNode()->GetId()));
	}
	_ui->webViewGraph->page()->mainFrame()->evaluateJavaScript(relGraphString);


}
/*!
 *
 */
void 
MainWindow::closeEvent(QCloseEvent* event) // 2.
{
	if (0)
	{
	int res = QMessageBox::warning(this, windowTitle(), "Are you sure?",
				QMessageBox::Yes|QMessageBox::No);
	if(res == QMessageBox::Yes)
		event->accept(); // 3.
	else
		event->ignore(); // 4.
	}
}