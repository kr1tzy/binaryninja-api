#pragma once

#include "uitypes.h"
#include <QtWidgets/QToolButton>
#include <QtCore/QParallelAnimationGroup>
#include <QtWidgets/QScrollArea>
#include <QtCore/QPropertyAnimation>

class BINARYNINJAUIAPI ExpandableGroup : public QWidget
{
	Q_OBJECT

private:
	QToolButton* m_button;
	QParallelAnimationGroup* m_animation;
	QScrollArea* m_content;
	QLayout* m_contentLayout;
	int m_duration = 100;

private Q_SLOTS:
	void toggled(bool expanded);

public:
	explicit ExpandableGroup(const QString& title = "", QWidget* parent = nullptr);
	void setContentWidget(QWidget* contentWidget);
	void setContentLayout(QLayout* contentLayout);
	void setTitle(const QString& title) { m_button->setText(title); }
	void toggle(bool expanded);
	void resizeLayout();
};